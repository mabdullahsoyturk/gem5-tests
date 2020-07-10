#!/bin/bash
# 
# Example job submission script
#
# TODO:
#   - Set the requested number of tasks (cpu cores) with --ntasks parameter.
#   - Select the partition (queue) you want to run the job in:
#     - short : For jobs that have maximum run time of 60 mins. Has higher priority.
#     - long  : For jobs that have maximum run time of 10 days. Lower priority than short.
#     - longer: For testing purposes, queue has 31 days limit but only two nodes.
#     - cuda  : For CUDA jobs. Solver that can utilize CUDA acceleration can use this queue. 5 days limit.
#   - Set the required time limit for the job with --time parameter.
#     - Acceptable time formats include "minutes", "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds"
#   - Put this script and all the input file under the same directory.
#   - Set the required parameters, input and output file names below.
#   - If you do not want mail please remove the line that has --mail-type
#   - Put this script and all the input file under the same directory.
#   - Submit this file using:
#      sbatch psiblast_submit.sh
#
# -= Resources =-
#
#SBATCH --job-name=gem5-bfs-biprp
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=8000
#SBATCH --time=5760
#SBATCH --output=%j-gem5bfs.out
#SBATCH --mail-type=ALL

echo "Running gem5 command..."
date
echo "Runs BFS application with dblp graph and Bimodal Interval Prediction replacement policy."
python3 launch.py --graph-name=dblp.el --app-name=bfs --l2_replacement=BIPRP
date
RET=$?

echo
echo "Solver exited with return code: $RET"
exit $RET

