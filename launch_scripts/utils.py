import os
import sys
import subprocess
from shutil import rmtree
import argparse

DYNAMIC_OPTIONS = {
    'write_buffer': ["4", "8", "16"],
    'mshr': ["4", "8", "16", "32"],
    'assoc': ["4", "8", "16", "32"],
    'prefetcher': ["TaggedPrefetcher", "DCPTPrefetcher", "IndirectMemoryPrefetcher", "SignaturePathPrefetcher"],
    'replacement': ["SecondChanceRP", "BIPRP", "LIPRP", "BRRIPRP"]   
}

DYNAMIC_OPTION_COMMANDS = {
    'write_buffer': '--l2_write_buffers=',
    'mshr': '--l2_mshrs=',
    'assoc': '--l2_assoc=',
    'prefetcher': '--l2-hwp-type=',
    'replacement': '--l2-replacement-policy='   
}

GEM5_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BENCH_BIN_DIR = GEM5_HOME + '/gapbs'
BENCH_GRAPH_DIR = BENCH_BIN_DIR + "/test/graphs/"

BENCH_BINARY = {
    'bc' : os.path.abspath(BENCH_BIN_DIR + '/bc'),
    'bfs': os.path.abspath(BENCH_BIN_DIR + '/bfs'),
    'cc' : os.path.abspath(BENCH_BIN_DIR + '/cc'),
    'cc_sv' : os.path.abspath(BENCH_BIN_DIR + '/cc_sv'),
    'pr' : os.path.abspath(BENCH_BIN_DIR + '/pr'),
    'sssp' : os.path.abspath(BENCH_BIN_DIR + '/sssp'),
    'tc' : os.path.abspath(BENCH_BIN_DIR + '/tc')
}

RESULTS_DIR = GEM5_HOME + "/results"
BENCH_RESULTS_DIR = {
    'bc' : RESULTS_DIR + '/bc',
    'bfs': RESULTS_DIR + '/bfs',
    'cc' : RESULTS_DIR + '/cc',
    'cc_sv' : RESULTS_DIR + '/cc_sv',
    'pr' : RESULTS_DIR + '/pr',
    'sssp' : RESULTS_DIR + '/sssp',
    'tc' : RESULTS_DIR + '/tc'
}

def compile_benchmarks():
    print("Compiling benchmarks")
    os.chdir(BENCH_BIN_DIR)        

    try:    
        subprocess.check_call(["make"], shell=True)
    except Exception as e:
        sys.exit(str(e))

    os.chdir(GEM5_HOME)

def clean_benchmarks():
    print("Cleaning benchmarks")
    os.chdir(BENCH_BIN_DIR)        

    try:    
        subprocess.check_call(["make clean"], shell=True)
    except Exception as e:
        sys.exit(str(e))
        
    os.chdir(GEM5_HOME)

def create_result_directories(bench_name):
    print("Creating result directories")
    if (not os.path.exists(RESULTS_DIR)):
        os.mkdir(RESULTS_DIR)

    if (not os.path.exists(BENCH_RESULTS_DIR[bench_name])):
        os.mkdir(BENCH_RESULTS_DIR[bench_name])

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bench-name', help='Benchmark\'s name', default='pr')
    parser.add_argument("--caches", action="store_true", default=True)
    parser.add_argument("--l2cache", action="store_true", default=True)
    parser.add_argument("--l2_size", default="4kB")
    parser.add_argument("--l2_assoc", default="2")
    parser.add_argument("--l1i_write_buffers", default="8")
    parser.add_argument("--l1d_write_buffers", default="8")
    parser.add_argument("--l2_write_buffers", default="8")
    parser.add_argument("--l1i_mshrs", default="4")
    parser.add_argument("--l1d_mshrs", default="4")
    parser.add_argument("--l2_mshrs", default="20")
    parser.add_argument("--l2_replacement", default="BRRIPRP")
    parser.add_argument("--mem-size", default="512MB")
    parser.add_argument("--graph", action="store_true", default=True)
    parser.add_argument("--graph-name", default="4.mtx")
    parser.add_argument("--static", action="store_true", default=False)
    parser.add_argument('--dynamic-option-name', default="base")

    return parser.parse_args()
