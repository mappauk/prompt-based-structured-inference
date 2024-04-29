#!/bin/bash
#SBATCH --qos=blanca-curc-gpu
#SBATCH --nodes=1
#SBATCH --job-name=moral-prompt
#SBATCH --ntasks=32
#SBATCH --gres=gpu:a100:1
#SBATCH --time=6:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8


conda activate moraldistill
python -m src.experiments.moral_foundation_identification_one_pass /rc_scratch/mapa7010/MoralDistillation/data /rc_scratch/mapa7010/MoralDistillation/output/onepassoutput.json
