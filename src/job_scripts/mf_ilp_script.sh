#!/bin/bash
#SBATCH --qos=blanca-curc-gpu
#SBATCH --nodes=1
#SBATCH --job-name=moral-prompt
#SBATCH --ntasks=64
#SBATCH --gres=gpu:a100:1
#SBATCH --time=09:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8
module load gcc/11.2.0


conda activate moraldistill
/rc_scratch/mapa7010/.conda/envs/moraldistill/bin/python -m src.experiments.moral_foundation_congress.moral_foundation_prompt_few_shot_mv /rc_scratch/mapa7010/MoralDistillation/data/moral_foundation_congress /rc_scratch/mapa7010/mistral_few_shot_mv_2_0.json /rc_scratch/mapa7010/MoralDistillation/data/few_shot_examples




