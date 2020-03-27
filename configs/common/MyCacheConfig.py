from __future__ import print_function, absolute_import

import m5
from m5.objects import *
from .Caches import *
from common import ObjectList

def config_cache(options, system):
    if options.external_memory_system and (options.caches or options.l2cache):
        print("External caches and internal caches are exclusive options.\n")
        sys.exit(1)

    dcache_class, icache_class, l2_cache_class, walk_cache_class = L1_DCache, L1_ICache, L2Cache, None

    # Set the cache line size of the system
    system.cache_line_size = options.cacheline_size

    if options.l2cache:
        # Provide a clock for the L2 and the L1-to-L2 bus here as they are not connected 
        # using addTwoLevelCacheHierarchy. Use the same clock as the CPUs.
        system.l2 = l2_cache_class(clk_domain=system.cpu_clk_domain, size=options.l2_size, assoc=options.l2_assoc, mshrs=options.l2_mshrs, write_buffers=options.l2_write_buffers)

        system.tol2bus = L2XBar(clk_domain = system.cpu_clk_domain)
        system.l2.cpu_side = system.tol2bus.master
        system.l2.mem_side = system.membus.slave
        if options.l2_hwp_type:
            hwpClass = ObjectList.hwp_list.get(options.l2_hwp_type)
            if system.l2.prefetcher != "Null":
                print("Warning: l2-hwp-type is set (", hwpClass, "), but",
                      "the current l2 has a default Hardware Prefetcher",
                      "of type", type(system.l2.prefetcher), ", using the",
                      "specified by the flag option.")
            system.l2.prefetcher = hwpClass()

    for i in range(options.num_cpus):
        if options.caches:
            icache = icache_class(size=options.l1i_size, assoc=options.l1i_assoc, mshrs=options.l1i_mshrs, write_buffers=options.l1i_write_buffers)
            dcache = dcache_class(size=options.l1d_size, assoc=options.l1d_assoc, mshrs=options.l1d_mshrs, write_buffers=options.l1d_write_buffers)

            # If we have a walker cache specified, instantiate two instances here
            iwalkcache, dwalkcache = None, None

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
            system.cpu[i].addPrivateSplitL1Caches(icache, dcache, iwalkcache, dwalkcache)

        system.cpu[i].createInterruptController()
        if options.l2cache:
            system.cpu[i].connectAllPorts(system.tol2bus, system.membus)
        else:
            system.cpu[i].connectAllPorts(system.membus)

    return system
