from __future__ import print_function, absolute_import

import optparse
import sys
import os

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath, fatal, warn

addToPath('../')

from common import MyOptions, Simulation, MyCacheConfig, CpuConfig, ObjectList, MemConfig
from common.FileSystemConfig import config_filesystem
from common.Caches import *
from common.cpu2000 import *

def get_processes(options):
    multiprocesses, pargs = [], []

    workloads = options.cmd.split(';')
    
    if options.options != "":
        pargs = options.options.split(';')

    process = Process(pid = 100)
    process.executable = workloads[0]
    process.cwd = os.getcwd()
    process.cmd = [workloads[0]] + pargs[0].split()

    multiprocesses.append(process)

    return multiprocesses

parser = optparse.OptionParser()
MyOptions.addCommonOptions(parser)
MyOptions.addSEOptions(parser)

(options, args) = parser.parse_args()

if args:
    print("Error: script doesn't take any positional arguments")
    sys.exit(1)

multiprocesses = []

if options.cmd:
    multiprocesses = get_processes(options)
else:
    print("No workload specified. Exiting!\n", file=sys.stderr)
    sys.exit(1)


(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(options)
CPUClass.numThreads = 1

np = options.num_cpus
system = System(cpu = [CPUClass(cpu_id=i) for i in range(np)], mem_mode = test_mem_mode,
                mem_ranges = [AddrRange(options.mem_size)], cache_line_size = options.cacheline_size)

# Create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = options.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock =  options.sys_clock, voltage_domain = system.voltage_domain)

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain()

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = options.cpu_clock, voltage_domain = system.cpu_voltage_domain)

# All cpus belong to a common cpu_clk_domain, therefore running at a common frequency.
for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain

for i in range(np):
    system.cpu[i].workload = multiprocesses[0]
    system.cpu[i].createThreads()

MemClass = Simulation.setMemClass(options)
system.membus = SystemXBar()
system.system_port = system.membus.slave
MyCacheConfig.config_cache(options, system)
MemConfig.config_mem(options, system)
config_filesystem(system, options)

root = Root(full_system = False, system = system)
Simulation.run(options, root, system, FutureClass)
