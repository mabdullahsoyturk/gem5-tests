import os
import sys
import subprocess
from shutil import rmtree
import argparse

kronecker_sizes = ["12","14", "16"]
# kronecker_sizes = ["2","4","6"]
l2_sizes = ["4kB", "16kB", "64kB", "256kB"]

WHERE_AM_I = os.path.dirname(os.path.realpath(__file__)) #  Absolute Path to *THIS* Script
BENCH_BIN_DIR = WHERE_AM_I + '/gapbs'
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

RESULTS_DIR = WHERE_AM_I + "/results"
BENCH_RESULTS_DIR = {
    'bc' : RESULTS_DIR + '/bc',
    'bfs': RESULTS_DIR + '/bfs',
    'cc' : RESULTS_DIR + '/cc',
    'cc_sv' : RESULTS_DIR + '/cc_sv',
    'pr' : RESULTS_DIR + '/pr',
    'sssp' : RESULTS_DIR + '/sssp',
    'tc' : RESULTS_DIR + '/tc'
}

def compileBenchmarks():
    print("Compiling benchmarks")
    os.chdir(BENCH_BIN_DIR)        

    try:    
        subprocess.check_call(["make"], shell=True)
    except Exception as e:
        sys.exit(str(e))

    os.chdir(WHERE_AM_I)

def cleanBenchmarks():
    print("Cleaning benchmarks")
    os.chdir(BENCH_BIN_DIR)        

    try:    
        subprocess.check_call(["make clean"], shell=True)
    except Exception as e:
        sys.exit(str(e))
        
    os.chdir(WHERE_AM_I)

def createResultDirectories(bench_name):
    print("Creating result directories")
    if (not os.path.exists(RESULTS_DIR)):
        os.mkdir(RESULTS_DIR)

    if (not os.path.exists(BENCH_RESULTS_DIR[bench_name])):
        os.mkdir(BENCH_RESULTS_DIR[bench_name])

        for kronecker_size in kronecker_sizes:
            if(not os.path.exists(BENCH_RESULTS_DIR[bench_name] + "/" + kronecker_size)):
                os.mkdir(BENCH_RESULTS_DIR[bench_name] + "/" + kronecker_size)
            
            for l2_size in l2_sizes:
                if(not os.path.exists(BENCH_RESULTS_DIR[bench_name] + "/" + kronecker_size + "/" + l2_size)):
                    os.mkdir(BENCH_RESULTS_DIR[bench_name] + "/" + kronecker_size + "/" + l2_size)

def removeResultDirectories(bench_name):
    for kronecker_size in kronecker_sizes:
        if (os.path.exists(BENCH_RESULTS_DIR[bench_name] + "/" + kronecker_size)):
            print("Deleting output directory for kronecker size {}".format(kronecker_size))
            rmtree(BENCH_RESULTS_DIR[bench_name] + "/" + kronecker_size)

def getBinaryOptions(args, kronecker_size):
    print("Here is the optinos")
    bench_binary_options = '"-f {}"'.format(BENCH_GRAPH_DIR + args.graph_name) if args.graph else '"-g {}"'.format(kronecker_size)
    print(bench_binary_options)
    return bench_binary_options

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bench-name', help='Benchmark\'s name', default='pr')
    parser.add_argument("--caches", action="store_true", default=True)
    parser.add_argument("--l2cache", action="store_true", default=True)
    parser.add_argument("--l2_size", default="64kB")
    parser.add_argument("--mem-size", default="512MB")
    parser.add_argument("--graph", action="store_true", default=False)
    parser.add_argument("--graph-name", default="4.mtx")

    return parser.parse_args()
