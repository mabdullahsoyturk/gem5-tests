from __future__ import print_function, absolute_import

import m5
from m5.objects import *
from gap_config import ObjectList

def config_cpus(options, system, multiprocesses):
    # All cpus belong to a common cpu_clk_domain, therefore running at a common frequency.
    for cpu in system.cpu:
        cpu.clk_domain = system.cpu_clk_domain

    for i in range(options.num_cpus):
        if len(multiprocesses) == 1:
            system.cpu[i].workload = multiprocesses[0]
        else:
            system.cpu[i].workload = multiprocesses[i]

        if options.bp_type:
            bpClass = ObjectList.bp_list.get(options.bp_type)
            system.cpu[i].branchPred = bpClass()

        if options.indirect_bp_type:
            indirectBPClass = \
                ObjectList.indirect_bp_list.get(options.indirect_bp_type)
            system.cpu[i].branchPred.indirectBranchPred = indirectBPClass()
            
        if options.numROBEntries:
            system.cpu[i].numROBEntries = options.numROBEntries;

        system.cpu[i].createThreads()
