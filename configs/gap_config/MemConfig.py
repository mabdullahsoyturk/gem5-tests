from __future__ import print_function, absolute_import
import m5.objects
from . import ObjectList
import math
from m5.util import fatal

def create_mem_ctrl(cls, r, i, nbr_mem_ctrls, intlv_bits, intlv_size):
    intlv_low_bit = int(math.log(intlv_size, 2))

    # Use basic hashing for the channel selection, and preferably use
    # the lower tag bits from the last level cache. As we do not know
    # the details of the caches here, make an educated guess. 4 MByte
    # 4-way associative with 64 byte cache lines is 6 offset bits and
    # 14 index bits.
    xor_low_bit = 20

    # Create an instance so we can figure out the address mapping and row-buffer size
    ctrl = cls()

    # Only do this for DRAMs
    if issubclass(cls, m5.objects.DRAMCtrl):
        # If the channel bits are appearing after the column
        # bits, we need to add the appropriate number of bits
        # for the row buffer size
        if ctrl.addr_mapping.value == 'RoRaBaChCo':
            # This computation only really needs to happen
            # once, but as we rely on having an instance we
            # end up having to repeat it for each and every
            # one
            rowbuffer_size = ctrl.device_rowbuffer_size.value * ctrl.devices_per_rank.value

            intlv_low_bit = int(math.log(rowbuffer_size, 2))

    # We got all we need to configure the appropriate address range
    ctrl.range = m5.objects.AddrRange(r.start, size = r.size(),
                                      intlvHighBit = intlv_low_bit + intlv_bits - 1,
                                      xorHighBit = xor_low_bit + intlv_bits - 1,
                                      intlvBits = intlv_bits,
                                      intlvMatch = i)
    return ctrl

def config_mem(options, system):
    """
    Create the memory controllers based on the options and attach them.
    If requested, we make a multi-channel configuration of the
    selected memory controller class by creating multiple instances of
    the specific class. The individual controllers have their
    parameters set such that the address range is interleaved between
    them.
    """

    # Mandatory options
    opt_mem_type = options.mem_type
    opt_mem_channels = options.mem_channels

    # Optional options
    opt_mem_ranks = getattr(options, "mem_ranks", None)
    opt_dram_powerdown = getattr(options, "enable_dram_powerdown", None)

    subsystem = system
    xbar = system.membus

    nbr_mem_ctrls = opt_mem_channels
    
    intlv_bits = int(math.log(nbr_mem_ctrls, 2))
    if 2 ** intlv_bits != nbr_mem_ctrls:
        fatal("Number of memory channels must be a power of 2")

    cls = ObjectList.mem_list.get(opt_mem_type)
    mem_ctrls = []

    # The default behaviour is to interleave memory channels on 128
    # byte granularity, or cache line granularity if larger than 128
    # byte. This value is based on the locality seen across a large
    # range of workloads.
    intlv_size = max(128, system.cache_line_size.value)

    # For every range (most systems will only have one), create an
    # array of controllers and set their parameters to match their
    # address mapping in the case of a DRAM
    for r in system.mem_ranges:
        for i in range(nbr_mem_ctrls):
            mem_ctrl = create_mem_ctrl(cls, r, i, nbr_mem_ctrls, intlv_bits,
                                       intlv_size)
            # Set the number of ranks based on the command-line
            # options if it was explicitly set
            if issubclass(cls, m5.objects.DRAMCtrl) and opt_mem_ranks:
                mem_ctrl.ranks_per_channel = opt_mem_ranks

            # Enable low-power DRAM states if option is set
            if issubclass(cls, m5.objects.DRAMCtrl):
                mem_ctrl.enable_dram_powerdown = opt_dram_powerdown

            mem_ctrls.append(mem_ctrl)

    subsystem.mem_ctrls = mem_ctrls

    # Connect the controllers to the membus
    for i in range(len(subsystem.mem_ctrls)):
        subsystem.mem_ctrls[i].port = xbar.master