#!/bin/bash
#SBATCH --qos=blanca-curc-gpu
#SBATCH --nodes=1
#SBATCH --job-name=coref-vc-llama
#SBATCH --ntasks=64
#SBATCH --gres=gpu:a100:1
#SBATCH --time=48:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8
module load gcc/11.2.0


conda activate llmsinf
/scratch/alpine/mapa7010/.conda/envs/llmsinf/bin/python -m src.experiments.coreference_resolution.coref_prompt_tf /scratch/alpine/mapa7010/MoralDistillation/data/coref/GENIA_MedCo_coreference_corpus_1.0/test/ /scratch/alpine/mapa7010/MoralDistillation/output/genia_vc/0/
## /scratch/alpine/mapa7010/.conda/envs/llmsinf/bin/python -m src.experiments.coreference_resolution.coref_prompt_tf /scratch/alpine/mapa7010/MoralDistillation/data/coref/conll-2012/v12/data/test/data/english/annotations/ /scratch/alpine/mapa7010/MoralDistillation/output/ontonotes_vc/0/