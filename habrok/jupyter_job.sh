#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=4
#SBATCH --time=02:00:00
#SBATCH --job-name=jupyter
#SBATCH --mem=8G
#SBATCH --partition=regular

module purge

module load Python/3.9.6-GCCcore-11.2.0

source ~/env/bin/activate

jupyter notebook --no-browser --ip=$( hostname )
