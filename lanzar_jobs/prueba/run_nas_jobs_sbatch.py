#!/usr/bin/env python3
import os
import subprocess
import shutil

def create_output_dirs(base_dir, config, iq_size, app_name):
    output_dir = os.path.join(base_dir, config, app_name, f"iq_{iq_size}")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    return output_dir

# TODO: Poner num_ticks o works 
def generate_sbatch_script(gem5_path, output_dir, config, iq_size, app_name, app_path, ckpt_path, partition="ce_100"):
    script_content = f"""#!/bin/bash
#SBATCH --partition={partition}
#SBATCH --job-name=gem5-{app_name}_{iq_size}
#SBATCH --output={output_dir}/slurm-%j.out

srun {gem5_path}build/X86/gem5.opt --outdir={output_dir} {gem5_path}tfg/board/configs/{config}-restore-checkpoint-splash.py \
--ckpt_path {ckpt_path} \
--application {app_path} \
--app_args "1 1" \
--num_cores 1 --mem_size 1 \
--works 2 \
--num_ticks 1000000000 \
--iq_size {iq_size}"""
    
    script_path = os.path.join(output_dir, "run.sbatch")
    with open(script_path, "w") as f:
        f.write(script_content)
    return script_path

def submit_job(script_path):
    subprocess.run(["sbatch", script_path])

def main():
    print("Ejecutando main")

    gem5_path = "/nfs/home/ce/alonsoge/gem5/"
    base_output_dir = "/nfs/home/ce/alonsoge/gem5/tfg/board/out/batch/NAS"
    ckpt_path = "/nfs/shared/ce/gem5/ckpts/x86/1core/1GB/NPB3.3-SER"
    app_dir = "/nfs/shared/ce/gem5/bin/NPB3.3-SER/"
    
    configs = ["bigO3", "smallO3"]
    iq_sizes = [32, 64, 128, 256, 512, 1024] 
    applications = [
        "bt.A.x", "bt.S.x", "bt.W.x", "cg.A.x", "cg.S.x", "cg.W.x", 
        "dc.S.x", "dc.W.x", "ep.A.x", "ep.S.x", "ep.W.x", 
        "ft.A.x", "ft.S.x", "ft.W.x", "is.A.x", "is.S.x", "is.W.x", 
        "lu.A.x", "lu.S.x", "lu.W.x", "mg.A.x", "mg.S.x", "mg.W.x", 
        "sp.A.x", "sp.S.x", "sp.W.x", "ua.A.x", "ua.S.x", "ua.W.x"
    ]
    for config in configs:
        for app in applications:
            app_path = os.path.join(app_dir, app)
            for iq_size in iq_sizes:
                output_dir = create_output_dirs(base_output_dir, config, iq_size, app)
                print(f"Ejecutando {app} con IQ de tamaño {iq_size} en {config}")
                sbatch_script = generate_sbatch_script(gem5_path, output_dir, config, iq_size, app, app_path, ckpt_path)
                submit_job(sbatch_script)

if __name__ == "__main__":
    main()

