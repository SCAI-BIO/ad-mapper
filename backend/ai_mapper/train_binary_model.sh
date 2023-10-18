#!/bin/bash
#
#SBATCH --job-name=run-mapping-model
#SBATCH --error=run-mapping-model.err
#SBATCH --output=run-mapping-model.out
#
#SBATCH --time=02:00:00
#SBATCH --gres=gpu:v100:1
#SBATCH --partition=gpu-mix

module load Anaconda3/2021.05
source activate ai-mapper_env

python3 train.py
