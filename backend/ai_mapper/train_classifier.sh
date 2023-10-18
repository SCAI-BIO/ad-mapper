#!/bin/bash
#
#SBATCH --job-name=run-mapping-model_cl
#SBATCH --error=run-mapping-model_cl.err
#SBATCH --output=run-mapping-model_cl.out
#
#SBATCH --time=1-00:00:00
#SBATCH --gres=gpu:a100:1
#SBATCH --partition=gpu-mix

module load Anaconda3/2021.05
source activate ai-mapper_env

python3 train_classifier.py
