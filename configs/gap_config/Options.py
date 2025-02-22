from __future__ import print_function
from __future__ import absolute_import

import m5
from m5.defines import buildEnv
from m5.objects import *

from . import ObjectList

def _listCpuTypes(option, opt, value, parser):
    ObjectList.cpu_list.print()
    sys.exit(0)

def _listBPTypes(option, opt, value, parser):
    ObjectList.bp_list.print()
    sys.exit(0)

def _listHWPTypes(option, opt, value, parser):
    ObjectList.hwp_list.print()
    sys.exit(0)

def _listIndirectBPTypes(option, opt, value, parser):
    ObjectList.indirect_bp_list.print()
    sys.exit(0)

def _listMemTypes(option, opt, value, parser):
    ObjectList.mem_list.print()
    sys.exit(0)

def _listPlatformTypes(option, opt, value, parser):
    ObjectList.platform_list.print()
    sys.exit(0)

# Add the very basic options that work also in the case of the no ISA
# being used, and consequently no CPUs, but rather various types of
# testers and traffic generators.
def addNoISAOptions(parser):
    parser.add_option("-n", "--num-cpus", type="int", default=1)
    parser.add_option("--sys-voltage", action="store", type="string",
                      default='1.0V',
                      help = """Top-level voltage for blocks running at system
                      power supply""")
    parser.add_option("--sys-clock", action="store", type="string",
                      default='1GHz',
                      help = """Top-level clock for blocks running at system
                      speed""")

    # CPU options
    parser.add_option("--numROBEntries", default=None)

    # Memory Options
    parser.add_option("--list-mem-types",
                      action="callback", callback=_listMemTypes,
                      help="List available memory types")
    parser.add_option("--mem-type", type="choice", default="DDR3_1600_8x8",
                      choices=ObjectList.mem_list.get_names(),
                      help = "type of memory to use")
    parser.add_option("--mem-channels", type="int", default=1,
                      help = "number of memory channels")
    parser.add_option("--mem-ranks", type="int", default=None,
                      help = "number of memory ranks per channel")
    parser.add_option("--mem-size", action="store", type="string",
                      default="512MB",
                      help="Specify the physical memory size (single memory)")
    parser.add_option("--enable-dram-powerdown", action="store_true",
                       help="Enable low-power states in DRAMCtrl")


    parser.add_option("--memchecker", action="store_true")

    # Cache Options
    parser.add_option("--caches", action="store_true")
    parser.add_option("--l2cache", action="store_true")
    parser.add_option("--num-dirs", type="int", default=1)
    parser.add_option("--num-l2caches", type="int", default=1)
    parser.add_option("--num-l3caches", type="int", default=1)
    parser.add_option("--l1d_size", type="string", default="64kB")
    parser.add_option("--l1i_size", type="string", default="32kB")
    parser.add_option("--l2_size", type="string", default="2MB")
    parser.add_option("--l3_size", type="string", default="16MB")
    parser.add_option("--l1d_assoc", type="int", default=2)
    parser.add_option("--l1i_assoc", type="int", default=2)
    parser.add_option("--l2_assoc", type="int", default=8)
    parser.add_option("--l3_assoc", type="int", default=16)
    parser.add_option("--l1d_mshrs", type="int", default=4)
    parser.add_option("--l1i_mshrs", type="int", default=4)
    parser.add_option("--l2_mshrs", type="int", default=20)
    parser.add_option("--l1d_write_buffers", type="int", default=8)
    parser.add_option("--l1i_write_buffers", type="int", default=8)
    parser.add_option("--l2_write_buffers", type="int", default=8)
    parser.add_option("--cacheline_size", type="int", default=64)

    # Run duration options
    parser.add_option("-m", "--abs-max-tick", type="int", default=m5.MaxTick,
                      metavar="TICKS", help="Run to absolute simulated tick "
                      "specified including ticks from a restored checkpoint")
    parser.add_option("--rel-max-tick", type="int", default=None,
                      metavar="TICKS", help="Simulate for specified number of"
                      " ticks relative to the simulation start tick (e.g. if "
                      "restoring a checkpoint)")
    parser.add_option("--maxtime", type="float", default=None,
                      help="Run to the specified absolute simulated time in "
                      "seconds")
    parser.add_option("-P", "--param", action="append", default=[],
        help="Set a SimObject parameter relative to the root node. "
             "An extended Python multi range slicing syntax can be used "
             "for arrays. For example: "
             "'system.cpu[0,1,3:8:2].max_insts_all_threads = 42' "
             "sets max_insts_all_threads for cpus 0, 1, 3, 5 and 7 "
             "Direct parameters of the root object are not accessible, "
             "only parameters of its children.")

# Add common options that assume a non-NULL ISA.
def addCommonOptions(parser):
    # start by adding the base options that do not assume an ISA
    addNoISAOptions(parser)

    # system options
    parser.add_option("--list-cpu-types",
                      action="callback", callback=_listCpuTypes,
                      help="List available CPU types")
    parser.add_option("--cpu-type", type="choice", default="AtomicSimpleCPU",
                      choices=ObjectList.cpu_list.get_names(),
                      help = "type of cpu to run with")
    parser.add_option("--list-bp-types",
                      action="callback", callback=_listBPTypes,
                      help="List available branch predictor types")
    parser.add_option("--list-indirect-bp-types",
                      action="callback", callback=_listIndirectBPTypes,
                      help="List available indirect branch predictor types")
    parser.add_option("--bp-type", type="choice", default=None,
                      choices=ObjectList.bp_list.get_names(),
                      help = """
                      type of branch predictor to run with
                      (if not set, use the default branch predictor of
                      the selected CPU)""")
    parser.add_option("--indirect-bp-type", type="choice", default=None,
                      choices=ObjectList.indirect_bp_list.get_names(),
                      help = "type of indirect branch predictor to run with")
    parser.add_option("--list-hwp-types",
                      action="callback", callback=_listHWPTypes,
                      help="List available hardware prefetcher types")
    parser.add_option("--l1i-hwp-type", type="choice", default=None,
                      choices=ObjectList.hwp_list.get_names(),
                      help = """
                      type of hardware prefetcher to use with the L1
                      instruction cache.
                      (if not set, use the default prefetcher of
                      the selected cache)""")
    parser.add_option("--l1d-hwp-type", type="choice", default=None,
                      choices=ObjectList.hwp_list.get_names(),
                      help = """
                      type of hardware prefetcher to use with the L1
                      data cache.
                      (if not set, use the default prefetcher of
                      the selected cache)""")
    parser.add_option("--l2-hwp-type", type="choice", default=None,
                      choices=ObjectList.hwp_list.get_names(),
                      help = """
                      type of hardware prefetcher to use with the L2 cache.
                      (if not set, use the default prefetcher of
                      the selected cache)""")
    parser.add_option("--l2-replacement-policy", type="choice", default=None,
                      choices=["FIFORP", "SecondChanceRP", "LFURP", "BIPRP", "LIPRP", "MRURP", "RandomRP", "BRRIPRP", "RRIPRP", "NRURP", "TreePLRURP", "WeightedLRURP"])
    parser.add_option("--checker", action="store_true");
    parser.add_option("--cpu-clock", action="store", type="string",
                      default='2GHz',
                      help="Clock for blocks running at CPU speed")
    parser.add_option("--smt", action="store_true", default=False,
                      help = """
                      Only used if multiple programs are specified. If true,
                      then the number of threads per cpu is same as the
                      number of programs.""")
    parser.add_option("--elastic-trace-en", action="store_true",
                      help="""Enable capture of data dependency and instruction
                      fetch traces using elastic trace probe.""")
    # Trace file paths input to trace probe in a capture simulation and input
    # to Trace CPU in a replay simulation
    parser.add_option("--inst-trace-file", action="store", type="string",
                      help="""Instruction fetch trace file input to
                      Elastic Trace probe in a capture simulation and
                      Trace CPU in a replay simulation""", default="")
    parser.add_option("--data-trace-file", action="store", type="string",
                      help="""Data dependency trace file input to
                      Elastic Trace probe in a capture simulation and
                      Trace CPU in a replay simulation""", default="")

    parser.add_option("-l", "--lpae", action="store_true")
    parser.add_option("-V", "--virtualisation", action="store_true")

    # Run duration options
    parser.add_option("-I", "--maxinsts", action="store", type="int",
                      default=None, help="""Total number of instructions to
                                            simulate (default: run forever)""")
    parser.add_option("--work-item-id", action="store", type="int",
                      help="the specific work id for exit & checkpointing")
    parser.add_option("--num-work-ids", action="store", type="int",
                      help="Number of distinct work item types")
    parser.add_option("--work-begin-cpu-id-exit", action="store", type="int",
                      help="exit when work starts on the specified cpu")
    parser.add_option("--work-end-exit-count", action="store", type="int",
                      help="exit at specified work end count")
    parser.add_option("--work-begin-exit-count", action="store", type="int",
                      help="exit at specified work begin count")
    parser.add_option("--init-param", action="store", type="int", default=0,
                      help="""Parameter available in simulation with m5
                              initparam""")
    parser.add_option("--initialize-only", action="store_true", default=False,
                      help="""Exit after initialization. Do not simulate time.
                              Useful when gem5 is run as a library.""")

    # Checkpointing options
    ###Note that performing checkpointing via python script files will override
    ###checkpoint instructions built into binaries.
    parser.add_option("--take-checkpoints", action="store", type="string",
        help="<M,N> take checkpoints at tick M and every N ticks thereafter")
    parser.add_option("--max-checkpoints", action="store", type="int",
        help="the maximum number of checkpoints to drop", default=5)
    parser.add_option("--checkpoint-dir", action="store", type="string",
        help="Place all checkpoints in this absolute directory")
    parser.add_option("-r", "--checkpoint-restore", action="store", type="int",
        help="restore from checkpoint <N>")
    parser.add_option("--checkpoint-at-end", action="store_true",
                      help="take a checkpoint at end of run")
    parser.add_option("--work-begin-checkpoint-count", action="store", type="int",
                      help="checkpoint at specified work begin count")
    parser.add_option("--work-end-checkpoint-count", action="store", type="int",
                      help="checkpoint at specified work end count")
    parser.add_option("--work-cpus-checkpoint-count", action="store", type="int",
                      help="checkpoint and exit when active cpu count is reached")
    parser.add_option("--restore-with-cpu", action="store", type="choice",
                      default="AtomicSimpleCPU",
                      choices=ObjectList.cpu_list.get_names(),
                      help = "cpu type for restoring from a checkpoint")


    # CPU Switching - default switch model goes from a checkpoint
    # to a timing simple CPU with caches to warm up, then to detailed CPU for
    # data measurement
    parser.add_option("--repeat-switch", action="store", type="int",
        default=None,
        help="switch back and forth between CPUs with period <N>")
    parser.add_option("-s", "--standard-switch", action="store", type="int",
        default=None,
        help="switch from timing to Detailed CPU after warmup period of <N>")
    parser.add_option("-p", "--prog-interval", type="str",
        help="CPU Progress Interval")


def addSEOptions(parser):
    # Benchmark options
    parser.add_option("-c", "--cmd", default="",
                      help="The binary to run in syscall emulation mode.")
    parser.add_option("-o", "--options", default="",
                      help="""The options to pass to the binary, use " "
                              around the entire string""")
    parser.add_option("-e", "--env", default="",
                      help="Initialize workload environment from text file.")
    parser.add_option("-i", "--input", default="",
                      help="Read stdin from a file.")
    parser.add_option("--output", default="",
                      help="Redirect stdout to a file.")
    parser.add_option("--errout", default="",
                      help="Redirect stderr to a file.")
    parser.add_option("--chroot", action="store", type="string", default=None,
                      help="The chroot option allows a user to alter the "    \
                           "search path for processes running in SE mode. "   \
                           "Normally, the search path would begin at the "    \
                           "root of the filesystem (i.e. /). With chroot, "   \
                           "a user can force the process to begin looking at" \
                           "some other location (i.e. /home/user/rand_dir)."  \
                           "The intended use is to trick sophisticated "      \
                           "software which queries the __HOST__ filesystem "  \
                           "for information or functionality. Instead of "    \
                           "finding files on the __HOST__ filesystem, the "   \
                           "process will find the user's replacment files.")
    parser.add_option("--interp-dir", action="store", type="string",
                      default=None,
                      help="The interp-dir option is used for "
                           "setting the interpreter's path. This will "
                           "allow to load the guest dynamic linker/loader "
                           "itself from the elf binary. The option points to "
                           "the parent folder of the guest /lib in the "
                           "host fs")

    parser.add_option("--redirects", action="append", type="string",
                      default=[],
                      help="A collection of one or more redirect paths "
                           "to be used in syscall emulation."
                           "Usage: gem5.opt [...] --redirects /dir1=/path/"
                           "to/host/dir1 --redirects /dir2=/path/to/host/dir2")