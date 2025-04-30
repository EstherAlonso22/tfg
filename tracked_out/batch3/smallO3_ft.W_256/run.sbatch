#!/bin/bash
#SBATCH --partition=ce_100
#SBATCH --job-name=ft.W.x_256
#SBATCH --output=/nfs/home/ce/alonsoge/gem5/tfg/out/batch/NAS/smallO3/ft.W.x/iq_256/slurm-%j.out

srun /nfs/home/ce/alonsoge/gem5/build/X86/gem5.opt --outdir=/nfs/home/ce/alonsoge/gem5/tfg/out/batch/NAS/smallO3/ft.W.x/iq_256 /nfs/home/ce/alonsoge/gem5/tfg/configs/restore-checkpoint.py --config smallO3 --ckpt_path /nfs/shared/ce/gem5/ckpts/x86/1core/1GB/NPB3.3-SER --application /nfs/shared/ce/gem5/bin/NPB3.3-SER/ft.W.x --num_cores 1 --mem_size 1 --works 10 --num_ticks 100000000000 --iq_size 256