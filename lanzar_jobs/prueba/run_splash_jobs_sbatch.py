#!/usr/bin/env python3
import os
import subprocess
import sys
sys.path.append("/nfs/home/ce/alonsoge/gem5/tfg/board/configs")
from SPLASH import getSplashPath, getSplashName
import shutil

def create_output_dirs(base_dir, config, iq_size, app_name):
    output_dir = os.path.join(base_dir, config, app_name, f"iq_{iq_size}")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    return output_dir

def cd_to_app_dir(app_base_dir, app):
    app_dir = getSplashPath(app)
    if app_dir is None:
        raise ValueError(f"Application directory for {app} not found.")
    os.chdir(os.path.join(app_base_dir, app_dir))
    return os.getcwd()

# TODO: Poner num_ticks o works 
def generate_sbatch_script(gem5_path, output_dir, config, iq_size, app_name, app_path, ckpt_path, partition="ce_100"):
    script_content = f"""#!/bin/bash
#SBATCH --partition={partition}
#SBATCH --job-name=gem5-{app_name}_{iq_size}
#SBATCH --output={output_dir}/slurm-%j.out

srun {gem5_path}build/X86/gem5.opt --outdir={output_dir} {gem5_path}tfg/board/configs/{config}-restore-checkpoint-splash.py \
--ckpt_path {ckpt_path} \
--application {app_path} \
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
    base_output_dir = "/nfs/home/ce/alonsoge/gem5/tfg/board/out/batch/SPLASH"
    ckpt_path = "/nfs/shared/ce/gem5/ckpts/x86/1core/1GB/SPLASH4"
    apps_base_dir = "/nfs/home/ce/alonsoge/Splash-4/Splash-4"
    
    configs = ["bigO3", "smallO3"]
    iq_sizes = [32, 64, 128, 256, 512, 1024] 
    applications = [
        "SPLASH4-BARNES",
        "SPLASH4-CHOLESKY",
        "SPLASH4-FFT",
        # "SPLASH4-FMM",
        # "SPLASH4-LU-CONT",
        # "SPLASH4-LU-NOCONT",
        # "SPLASH4-OCEAN-CONT",
        # "SPLASH4-OCEAN-NOCONT",
        # "SPLASH4-RADIOSITY",
        # "SPLASH4-RADIX",
        # "SPLASH4-RAYTRACE",
        # "SPLASH4-VOLREND",
        # "SPLASH4-VOLREND-NPL",
        "SPLASH4-WATER-NSQUARED",
        # "SPLASH4-WATER-SPATIAL",
]
    for config in configs:
        for app in applications:
            app_name = getSplashName(app)
            app_dir = cd_to_app_dir(apps_base_dir, app)
            app_path = os.path.join(app_dir, app)
            for iq_size in iq_sizes:
                output_dir = create_output_dirs(base_output_dir, config, iq_size, app_name)
                print(f"Directorio actual: {os.getcwd()}")
                sbatch_script = generate_sbatch_script(gem5_path, output_dir, config, iq_size, app, app_path, ckpt_path)
                submit_job(sbatch_script)

if __name__ == "__main__":
    main()

