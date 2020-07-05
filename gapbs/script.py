import os
import sys
import subprocess
from functools import partial
import concurrent.futures 
from os.path import dirname as up

WHERE_AM_I = up(os.path.realpath(__file__)) #  Absolute Path to *THIS* Script
GEM5_PATH = up(WHERE_AM_I) + "/gem5-riscv"
GEM5_BINARY = GEM5_PATH + "/build/RISCV/gem5.opt"
GEM5_SCRIPT = GEM5_PATH + "/configs/example/se.py"

class ExperimentManager:
    ##
    #  example gem5 run:
    #    <gem5 bin> <gem5 options> <gem5 script> <gem5 script options>
    ##
    def __init__(self, kronecker_g, num_of_cpu, mem_size="512MB"):
        self.kronecker_g = kronecker_g
        self.num_of_cpu = num_of_cpu
        self.mem_size = mem_size

    def run(self):
        redirection = '-re'
        outdir = '--outdir=results/' + self.kronecker_g
        stdout_file = '--stdout-file=output.txt'
        stderr_file = '--stderr-file=error.txt'

        gem5_option = ' '.join([redirection, outdir, stdout_file, stderr_file])

        bench_binary_path = '-c ' + WHERE_AM_I + "/pr"

        bench_binary_options = '-o "' + '-g ' + self.kronecker_g + '"'

        gem5_script_option = ' '.join([bench_binary_path, bench_binary_options, "--caches", "--l2cache", "--mem-size=" + self.mem_size])

        gem5_command = ' '.join([GEM5_BINARY, gem5_option, GEM5_SCRIPT, gem5_script_option])

        try:    
            subprocess.check_call(gem5_command, shell=True)
        except Exception as e:
            sys.exit(str(e))

def run_experiment(g_values):
    experiment_manager = ExperimentManager(str(g_values), 4)
    experiment_manager.run()

if __name__ == "__main__":
    g_values = [g for g in range(4,35,2)]

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor: 
        executor.map(run_experiment, g_values)