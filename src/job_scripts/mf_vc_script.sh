#!/bin/bash
#SBATCH --qos=blanca-curc-gpu
#SBATCH --nodes=1
#SBATCH --job-name=mf-vc-llama
#SBATCH --ntasks=64
#SBATCH --gres=gpu:a100:1
#SBATCH --time=48:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8
module load gcc/11.2.0


conda activate llmsinf
/scratch/alpine/mapa7010/.conda/envs/llmsinf/bin/python -m src.experiments.moral_foundation_congress.mf_prompt_vc /scratch/alpine/mapa7010/MoralDistillation/data/moral_foundation_congress /scratch/alpine/mapa7010/MoralDistillation/output/mf_llama_vc/