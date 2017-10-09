#!/bin/bash
#SBATCH -J {run_id}_$SLURM_ARRAY_TASK_ID
#SBATCH -o log_slurm.{run_id}_$SLURM_ARRAY_TASK_ID.out
#SBATCH -n 1
#SBATCH --cpus-per-task={threads}
#SBATCH --array=0-{jobs}
#SBATCH -p {queue}
#SBATCH -t 12:00:00

module load {modules}

