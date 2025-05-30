#!/bin/bash

#SBATCH --qos=blanca-blast-lecs
#SBATCH --partition=blanca-blast-lecs
#SBATCH --account=blanca-blast-lecs
#SBATCH --nodes=1
#SBATCH --job-name=mf-llama-structured-ft
#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=4000m
#SBATCH --gres=gpu:h100_3g.40gb
#SBATCH --time=60:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8
module load gcc/11.2.0
conda activate llmsinf

/scratch/alpine/mapa7010/.conda/envs/llmsinf/bin/python -m src.learning.llm_structured_ft_training /scratch/alpine/mapa7010/MoralDistillation/data/moral_foundation_congress/ /scratch/alpine/mapa7010/MoralDistillation/output/mf_llama_mc/5/ /scratch/alpine/mapa7010/MoralDistillation/output/mf_logreg_calib_checkpoint/ mc /scratch/alpine/mapa7010/MoralDistillation/output/mf_llama_sft_mc_combo/ /scratch/alpine/mapa7010/MoralDistillation/output/structured_ft_checkpoint_1/