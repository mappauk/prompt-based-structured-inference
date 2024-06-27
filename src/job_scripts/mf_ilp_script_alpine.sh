#!/bin/bash
#SBATCH --qos=normal
#SBATCH --partition=aa100
#SBATCH --nodes=1
#SBATCH --job-name=moral-prompt
#SBATCH --ntasks=32
#SBATCH --gres=gpu:a100:1
#SBATCH --time=24:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8


conda activate moraldistill
/rc_scratch/mapa7010/.conda/envs/moraldistill/bin/python -m src.experiments.moral_foundation_prompt_ilp /rc_scratch/mapa7010/MoralDistillation/data /rc_scratch/mapa7010/ilp_output.json /rc_scratch/mapa7010/MoralDistillation/data/few_shot_examples
