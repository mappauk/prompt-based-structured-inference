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
/rc_scratch/mapa7010/.conda/envs/moraldistill/bin/python -m src.experiments.coreference_resolution.coref_resolution_prompt_few_shot_tf /rc_scratch/mapa7010/MoralDistillation/data/coref/GENIA_MedCo_coreference_corpus_1.0/test /rc_scratch/mapa7010/mistral_coref_few_shot_tf_0_2.json /rc_scratch/mapa7010/MoralDistillation/data/few_shot_examples/genia_coref_examples.json




