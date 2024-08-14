#!/bin/bash
#SBATCH --qos=blanca-curc-gpu
#SBATCH --nodes=1
#SBATCH --job-name=moral-prompt
#SBATCH --ntasks=64
#SBATCH --gres=gpu:a100:1
#SBATCH --time=72:00:00

module purge
module load python/3.8.0
module load anaconda
module load cuda/11.8


conda activate moraldistill
/rc_scratch/mapa7010/.conda/envs/moraldistill/bin/python -m src.experiments.coreference_resolution.coref_resolution_prompt_ilp_tf /rc_scratch/mapa7010/MoralDistillation/data/coref/GENIA_MedCo_coreference_corpus_1.0/test /rc_scratch/mapa7010/coref_genia_ilp_tf_one.json /rc_scratch/mapa7010/MoralDistillation/data/few_shot_examples/genia_coref_examples.json
