import os
import sys
import utils
import subprocess
import concurrent.futures
from functools import partial

GEM5_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

BENCH_BIN_DIR = GEM5_HOME + '/gapbs'
BENCH_GRAPH_DIR = BENCH_BIN_DIR + "/test/graphs/"

GEM5_BINARY = os.path.abspath(GEM5_HOME + '/build/RISCV/gem5.fast')
GEM5_SCRIPT = os.path.abspath(GEM5_HOME + '/configs/gap_config/run.py')

class ExperimentManager:
    # <gem5 bin> <gem5 options> <gem5 script> <benchmark path> <benchmark options> <gem5 script options>
    def __init__(self):
        self.args = args

    def launch(self, dynamic_option=None):
        gem5_options = self.get_gem5_options(dynamic_option)
        benchmark_path = self.get_benchmark_path()
        benchmark_options = self.get_benchmark_options()
        gem5_script_options = self.get_gem5_script_options(dynamic_option)

        gem5_command = ' '.join([GEM5_BINARY, gem5_options, GEM5_SCRIPT, benchmark_path, benchmark_options, gem5_script_options])

        try:    
            print("Started executing: \n\n{}".format(gem5_command))
            subprocess.check_call(gem5_command, shell=True)
            print("Finished executing: \n\n{}".format(gem5_command))
        except Exception as e:
            sys.exit(str(e))
    
    def get_gem5_options(self, dynamic_option):
        redirection = '-re'
        graph_name = self.args.graph_name
        if dynamic_option:
            outdir = '--outdir={}/results/{}/{}/{}/{}'.format(GEM5_HOME, self.args.app_name, graph_name, self.args.dynamic_option_name, dynamic_option)
        else:
            outdir = '--outdir={}/results/{}/{}/base_result'.format(GEM5_HOME, self.args.app_name, graph_name)
        stdout_file = '--stdout-file=output.txt'
        stderr_file = '--stderr-file=error.txt'

        return ' '.join([redirection, outdir, stdout_file, stderr_file])

    def get_benchmark_path(self):
        return '-c ' + utils.BENCH_BINARY[self.args.app_name]

    def get_benchmark_options(self):
        benchmark_options = '-o "-f {}"'.format(BENCH_GRAPH_DIR + self.args.graph_name)
        return benchmark_options

    def get_gem5_script_options(self, dynamic_option):
        cpu_options = "--cpu-type=DerivO3CPU -n {}".format(self.args.num_cpus)
        l1cache_options = '--caches --l1d_size={} --l1i_size={}'.format(self.args.l1d_size, self.args.l1i_size)
        l2cache_options = '--l2cache --l2_size={}'.format(self.args.l2_size)
        memory_options = '--mem-size={}'.format(self.args.mem_size)
        l1_mshr_options = '--l1i_mshrs={} --l1d_mshrs={}'.format(self.args.l1i_mshrs, self.args.l1d_mshrs)
        l1_write_buffer_options = ' --l1i_write_buffers={} --l1d_write_buffers={}'.format(self.args.l1i_write_buffers, self.args.l1d_write_buffers)
        if dynamic_option:
            l2_dynamic_option = self.get_dynamic_option_command(dynamic_option)
        else:
            l2_dynamic_option = ''
        return ' '.join([cpu_options, l1cache_options, l2cache_options, memory_options, l1_mshr_options, l1_write_buffer_options, l2_dynamic_option])

    def get_dynamic_option_command(self, dynamic_option):
        return utils.DYNAMIC_OPTION_COMMANDS[self.args.dynamic_option_name] + dynamic_option

def run_experiment(dynamic_option, experiment_manager, args):
    experiment_manager.launch(dynamic_option)

if __name__ == "__main__":
    args = utils.get_arguments()
    utils.create_result_directories(args.app_name)

    experiment_manager = ExperimentManager()

    if args.dynamic_option_name:
        method_with_args = partial(run_experiment, experiment_manager=experiment_manager, args=args)
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            executor.map(method_with_args, utils.DYNAMIC_OPTIONS[args.dynamic_option_name])
    else:
        experiment_manager.launch()