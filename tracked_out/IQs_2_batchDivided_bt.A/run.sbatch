#!/bin/bash
#SBATCH --partition=ce_100
#SBATCH --job-name=bt.A.x_900
#SBATCH --output=/nfs/home/ce/alonsoge/gem5/tfg/out/batch-Dividida-IQmax/NAS/generalBigO3/bt.A.x/IQs_2/slurm-%j.out

srun /nfs/home/ce/alonsoge/gem5/build/X86/gem5.opt --outdir=/nfs/home/ce/alonsoge/gem5/tfg/out/batch-Dividida-IQmax/NAS/generalBigO3/bt.A.x/IQs_2 /nfs/home/ce/alonsoge/gem5/tfg/configs/restore-checkpoint-divided.py --config generalBigO3 --ckpt_path /nfs/shared/ce/gem5/ckpts/x86/1core/1GB/NPB3.3-SER --application /nfs/shared/ce/gem5/bin/NPB3.3-SER/bt.A.x --num_cores 1 --mem_size 1 --works 2 --num_ticks 50000000000 --iq_size 900 --num_IQs 2 --num_DividedIQ_entries 450