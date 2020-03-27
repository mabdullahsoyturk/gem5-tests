import os
import sys
import launch_utils
import subprocess
import concurrent.futures
from functools import partial

WHERE_AM_I = os.path.dirname(os.path.realpath(__file__)) #  Absolute Path to *THIS* Script

BENCH_INPUT_HOME = WHERE_AM_I + '/inputs'
BENCH_BIN_HOME = WHERE_AM_I + '/gapbs'

GEM5_BINARY = os.path.abspath(WHERE_AM_I + '/build/RISCV/gem5.fast')
GEM5_SCRIPT = os.path.abspath(WHERE_AM_I + '/configs/example/se.py')

class ExperimentManager:
    # <gem5 bin> <gem5 options> <gem5 script> <gem5 script options>
    # build/RISCV/gem5.opt <gem5 options> configs/example/se.py --cpu-type=DerivO3CPU -n 4
    # -c <app path> -o "app opts"
    # --caches --l1d_size=<size> --l1i_size=<size> --l2cache --l2_size=<size> --mem-size=<size>

    def __init__(self, kronecker_size, args):
        self.kronecker_size = kronecker_size
        self.args = args

    def launch(self, l2_size):
        redirection = '-re'
        graph_name = self.args.graph_name if self.args.graph else self.kronecker_size
        outdir = '--outdir=' + WHERE_AM_I + "/results/" + self.args.bench_name + "/" + graph_name + "/" + l2_size
        stdout_file = '--stdout-file=output.txt'
        stderr_file = '--stderr-file=error.txt'

        gem5_options = ' '.join([redirection, outdir, stdout_file, stderr_file])
        bench_binary_path = '-c ' + launch_utils.BENCH_BINARY[self.args.bench_name]

        bench_binary_options = '-o ' + launch_utils.getBinaryOptions(self.args, self.kronecker_size)
        print(bench_binary_options)
        other_script_options = '--caches --l1d_size=2kB --l1i_size=2kB --cpu-type=DerivO3CPU -n 4 --mem-size=' + self.args.mem_size
        other_script_options += ' --l2cache --l2_size=' + l2_size

        gem5_script_option = ' '.join([bench_binary_path, bench_binary_options, other_script_options])

        gem5_command = ' '.join([GEM5_BINARY, gem5_options, GEM5_SCRIPT, gem5_script_option])
        print("Working command: \n\n" + gem5_command)

        try:    
            print("\n\nStarted with l2cache: {} ".format(l2_size))
            subprocess.check_call(gem5_command, shell=True)
            print("Finished with l2cache: {} ".format(l2_size))
        except Exception as e:
            sys.exit(str(e))

def run_experiment(l2_size, experiment_manager, args):
    experiment_manager.launch(l2_size)

if __name__ == "__main__":
    args = launch_utils.get_arguments()

    #launch_utils.cleanBenchmarks()
    #launch_utils.compileBenchmarks()
    launch_utils.removeResultDirectories(args.bench_name)
    launch_utils.createResultDirectories(args.bench_name)

    if args.graph:
        experiment_manager = ExperimentManager(0,args)
        method_with_args = partial(run_experiment, experiment_manager=experiment_manager, args=args)
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            executor.map(method_with_args, launch_utils.l2_sizes)
    else:
        for kronecker_size in launch_utils.kronecker_sizes:
            experiment_manager = ExperimentManager(kronecker_size, args)
            method_with_args = partial(run_experiment, experiment_manager=experiment_manager, args=args)
            with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
                executor.map(method_with_args, launch_utils.l2_sizes)
