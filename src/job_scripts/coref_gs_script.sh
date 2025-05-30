#!/bin/bash
#SBATCH --qos=blanca-curc-gpu
#SBATCH --nodes=1
#SBATCH --job-name=coref-gs-llama
#SBATCH --ntasks=64
#SBATCH --gres=gpu:a100:1
#SBATCH --time=48:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8
module load gcc/11.2.0


conda activate llmsinf
/scratch/alpine/mapa7010/.conda/envs/llmsinf/bin/python -m src.experiments.coreference_resolution.coref_prompt_gs /scratch/alpine/mapa7010/MoralDistillation/data/coref/GENIA_MedCo_coreference_corpus_1.0/test/ /scratch/alpine/mapa7010/MoralDistillation/output/genia_gs/0/ /scratch/alpine/mapa7010/MoralDistillation/data/few_shot_examples/genia_coref_examples.json 0
## /scratch/alpine/mapa7010/.conda/envs/llmsinf/bin/python -m src.experiments.coreference_resolution.coref_prompt_gs /scratch/alpine/mapa7010/MoralDistillation/data/coref/conll-2012/v12/data/test/data/english/annotations/ /scratch/alpine/mapa7010/MoralDistillation/output/ontonotes_gs/0/ /scratch/alpine/mapa7010/MoralDistillation/data/few_shot_examples/ontonotes_coref_examples.json 0