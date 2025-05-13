#!/bin/bash
#SBATCH --partition=ce_100
#SBATCH --job-name=bt.W.x_900
#SBATCH --output=/nfs/home/ce/alonsoge/gem5/tfg/out/batch/NAS/generalO3/bt.W.x/iq_900/IQs_1/slurm-%j.out

srun /nfs/home/ce/alonsoge/gem5/build/X86/gem5.opt --outdir=/nfs/home/ce/alonsoge/gem5/tfg/out/batch/NAS/generalO3/bt.W.x/iq_900/IQs_1 /nfs/home/ce/alonsoge/gem5/tfg/configs/restore-checkpoint.py --config generalO3 --ckpt_path /nfs/shared/ce/gem5/ckpts/x86/1core/1GB/NPB3.3-SER --application /nfs/shared/ce/gem5/bin/NPB3.3-SER/bt.W.x --num_cores 1 --mem_size 1 --works 10 --num_ticks 100000000000 --iq_size 900 --num_IQs 1 --num_ports 12 --num_DividedIQ_entries 900
