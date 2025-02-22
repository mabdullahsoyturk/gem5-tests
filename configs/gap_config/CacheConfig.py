from __future__ import print_function, absolute_import

import m5
from m5.objects import *
from .Caches import *
from gap_config import ObjectList

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

def config_cache(options, system):
    dcache_class, icache_class, l2_cache_class = L1_DCache, L1_ICache, L2Cache

    # Set the cache line size of the system
    system.cache_line_size = options.cacheline_size

    if options.l2cache:
        if options.l2_replacement_policy != None:
            l2_replacement_policy = replacement_policies[options.l2_replacement_policy] 
            system.l2 = l2_cache_class(clk_domain=system.cpu_clk_domain, size=options.l2_size, assoc=options.l2_assoc, 
                                    mshrs=options.l2_mshrs, write_buffers=options.l2_write_buffers, replacement_policy=l2_replacement_policy)
        else:
            system.l2 = l2_cache_class(clk_domain=system.cpu_clk_domain, size=options.l2_size, assoc=options.l2_assoc, 
                                mshrs=options.l2_mshrs, write_buffers=options.l2_write_buffers)
        system.tol2bus = L2XBar(clk_domain = system.cpu_clk_domain)
        system.l2.cpu_side = system.tol2bus.master
        system.l2.mem_side = system.membus.slave
        if options.l2_hwp_type:
            hwpClass = ObjectList.hwp_list.get(options.l2_hwp_type)
            system.l2.prefetcher = hwpClass()

    for i in range(options.num_cpus):
        if options.caches:
            icache = icache_class(size=options.l1i_size, assoc=options.l1i_assoc, mshrs=options.l1i_mshrs, write_buffers=options.l1i_write_buffers, writeback_clean=True)
            dcache = dcache_class(size=options.l1d_size, assoc=options.l1d_assoc, mshrs=options.l1d_mshrs, write_buffers=options.l1d_write_buffers, writeback_clean=True)

            if options.l1d_hwp_type:
                hwpClass = ObjectList.hwp_list.get(options.l1d_hwp_type)
                if dcache.prefetcher != m5.params.NULL:
                    print("Warning: l1d-hwp-type is set (", hwpClass, "), but",
                          "the current l1d has a default Hardware Prefetcher",
                          "of type", type(dcache.prefetcher), ", using the",
                          "specified by the flag option.")
                dcache.prefetcher = hwpClass()

            if options.l1i_hwp_type:
                hwpClass = ObjectList.hwp_list.get(options.l1i_hwp_type)
                if icache.prefetcher != m5.params.NULL:
                    print("Warning: l1i-hwp-type is set (", hwpClass, "), but",
                          "the current l1i has a default Hardware Prefetcher",
                          "of type", type(icache.prefetcher), ", using the",
                          "specified by the flag option.")
                icache.prefetcher = hwpClass()

            # When connecting the caches, the clock is also inherited from the CPU in question
            system.cpu[i].addPrivateSplitL1Caches(icache, dcache)

        system.cpu[i].createInterruptController()
        if options.l2cache:
            system.cpu[i].connectAllPorts(system.tol2bus, system.membus)
        else:
            system.cpu[i].connectAllPorts(system.membus)

    return system
