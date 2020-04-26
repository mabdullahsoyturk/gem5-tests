import concurrent.futures
import launch_utils

def run_experiment(l2_prefecther):
    print(l2_prefecther)

if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(run_experiment, launch_utils.l2_prefecthers)