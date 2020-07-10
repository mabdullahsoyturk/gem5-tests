import m5
from m5.objects import *
from . import ObjectList

replacement_policies = {
    "FIFORP": FIFORP(),
    "SecondChanceRP": SecondChanceRP(),
    "LFURP": LFURP(),
    "BIPRP": BIPRP(),
    "LIPRP": LIPRP(),
    "MRURP": MRURP(),
    "RandomRP": RandomRP(),
    "BRRIPRP": BRRIPRP(),
    "RRIPRP": RRIPRP(),
    "NRURP": NRURP(),
    "TreePLRURP": TreePLRURP(),
    "WeightedLRURP": WeightedLRURP()
}

def getCPUClass(cpu_type):
    cls = ObjectList.cpu_list.get(cpu_type)
    return cls

def getMemoryMode(cpu_type):
    cls = ObjectList.cpu_list.get(cpu_type)
    return cls.memory_mode()

def getProcesses(options):
    """Interprets provided options and returns a list of processes"""

    multiprocesses = []
    inputs = []
    outputs = []
    errouts = []
    pargs = []

    workloads = options.cmd.split(';')
    if options.input != "":
        inputs = options.input.split(';')
    if options.output != "":
        outputs = options.output.split(';')
    if options.errout != "":
        errouts = options.errout.split(';')
    if options.options != "":
        pargs = options.options.split(';')

    idx = 0
    for wrkld in workloads:
        process = Process(pid = 100 + idx)
        process.executable = wrkld
        process.cwd = os.getcwd()

        if options.env:
            with open(options.env, 'r') as f:
                process.env = [line.rstrip() for line in f]

        if len(pargs) > idx:
            process.cmd = [wrkld] + pargs[idx].split()
        else:
            process.cmd = [wrkld]

        if len(inputs) > idx:
            process.input = inputs[idx]
        if len(outputs) > idx:
            process.output = outputs[idx]
        if len(errouts) > idx:
            process.errout = errouts[idx]

        multiprocesses.append(process)
        idx += 1

    return multiprocesses