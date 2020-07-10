from __future__ import print_function, absolute_import

import os, sys, optparse

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath, fatal, warn

addToPath('../')

from gap_config import Options, CPUConfig, CacheConfig, ObjectList, MemConfig, FileSystemConfig
from gap_config.Utils import getProcesses, getCPUClass, getMemoryMode

parser = optparse.OptionParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)

(options, args) = parser.parse_args()

if options.cmd:
    multiprocesses = getProcesses(options)
else:
    print("No workload specified. Exiting!\n", file=sys.stderr)
    sys.exit(1)

CPUClass = getCPUClass(options.cpu_type)
mem_mode = getMemoryMode(options.cpu_type)

number_of_cpus = options.num_cpus
system = System(cpu = [CPUClass(cpu_id=i) for i in range(number_of_cpus)],
                mem_mode = mem_mode,
                mem_ranges = [AddrRange(options.mem_size)],
                cache_line_size = options.cacheline_size)

# Create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = options.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock =  options.sys_clock, voltage_domain = system.voltage_domain)

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain()

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = options.cpu_clock, voltage_domain = system.cpu_voltage_domain)

system.membus = SystemXBar()
system.system_port = system.membus.slave

CPUConfig.config_cpus(options, system, multiprocesses)
CacheConfig.config_cache(options, system)
MemConfig.config_mem(options, system)
FileSystemConfig.config_filesystem(system, options)

# All scripts must have a root
root = Root(full_system = False, system = system)

# This is where all the C++ objects are created
m5.instantiate()

print("**** SIMULATIONS STARTS ****")
exit_event = m5.simulate()
print("**** SIMULATIONS ENDS ****")
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))