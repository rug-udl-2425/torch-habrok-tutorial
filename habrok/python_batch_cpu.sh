#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --job-name=cpu_job
#SBATCH --mem=8000

module purge

module load Python/3.9.6-GCCcore-11.2.0

source ~/env/bin/activate

python demo.py
