#!/bin/bash
#SBATCH --qos=blanca-curc-gpu
#SBATCH --nodes=1
#SBATCH --job-name=moral-prompt
#SBATCH --ntasks=64
#SBATCH --gres=gpu:a100:1
#SBATCH --time=30:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8
module load gcc/11.2.0


conda activate moraldistill
/rc_scratch/mapa7010/.conda/envs/moraldistill/bin/python -m src.experiments.genz_test /rc_scratch/mapa7010/genz_test_output.json
