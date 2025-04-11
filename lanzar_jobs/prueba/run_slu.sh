#!/bin/bash
#SBATCH --job-name=gem5_run
#SBATCH --partition=ce_100
#SBATCH --nodelist=ce100,ce101
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1

srun --ntasks=1 build/X86/gem5.opt -re \
    --outdir=tfg/board/out/volrend-npl \
    tfg/board/configs/take-checkpoint-stats-splash.py \
    --ckpt_path tfg/prueba_ckpts/ckpt/ \
    --application ../Splash-4/Splash-4/volrend/VOLREND-NPL \
    --app_args "1 inputs/head 8" \
    --num_cores 1 --mem_size 1

srun --ntasks=1 build/X86/gem5.opt -re \
    --outdir=tfg/board/out/volrend \
    tfg/board/configs/take-checkpoint-stats-splash.py \
    --ckpt_path tfg/prueba_ckpts/ckpt/ \
    --application ../Splash-4/Splash-4/volrend/VOLREND \
    --app_args "1 inputs/head 8" \
    --num_cores 1 --mem_size 1
