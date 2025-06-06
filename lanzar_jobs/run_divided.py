#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil
import argparse
import math

sys.path.append("/nfs/home/ce/alonsoge/gem5/tfg/configs")
from SPLASH import getSplashPath, getSplashName
import time

def create_directory(path, clean_if_exists=False):
    """Create a directory, optionally cleaning it if it already exists."""
    if clean_if_exists and os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    return path

def resolve_app_directory(base_dir, app):
    """Resolve the application directory and change to it."""
    app_dir = getSplashPath(app)
    if app_dir is None:
        raise ValueError(f"Application directory for {app} not found.")
    full_path = os.path.join(base_dir, app_dir)
    os.chdir(full_path)
    return full_path

def generate_sbatch_script(gem5_path, output_dir, config, iq_size, app_name, app_path, ckpt_path, num_ticks, num_IQs, entries_per_IQ, partition="ce_200"):
    """Generate the sbatch script for the job."""
    script_content = f"""#!/bin/bash
#SBATCH --partition={partition}
#SBATCH --job-name={app_name}_{num_IQs}
#SBATCH --output={output_dir}/slurm-%j.out

srun {gem5_path}build/X86/gem5.opt --outdir={output_dir} --debug-flags=DividedIQ {gem5_path}tfg/configs/restore-checkpoint-divided.py \
--config {config} \
--ckpt_path {ckpt_path} \
--application {app_path} \
--num_cores 1 --mem_size 1 \
--works 2 \
--num_ticks {num_ticks} \
--iq_size {iq_size} \
--num_IQs {num_IQs} \
--num_DividedIQ_entries {entries_per_IQ}"""
    
    script_path = os.path.join(output_dir, "run.sbatch")
    with open(script_path, "w") as f:
        f.write(script_content)
    return script_path

def submit_job(script_path):
    """Submit the job using sbatch."""
    subprocess.run(["sbatch", script_path])

def get_applications_by_benchmark(benchmark):
    """Retrieve the list of applications for a given benchmark."""
    benchmarks = {
        "SPLASH": [
            "SPLASH4-BARNES", "SPLASH4-CHOLESKY", "SPLASH4-FFT", "SPLASH4-FMM", 
            "SPLASH4-LU-CONT", "SPLASH4-LU-NOCONT", "SPLASH4-OCEAN-CONT", 
            "SPLASH4-OCEAN-NOCONT", "SPLASH4-RADIOSITY", "SPLASH4-RAYTRACE", 
            "SPLASH4-RADIX", "SPLASH4-VOLREND", "SPLASH4-VOLREND-NPL", 
            "SPLASH4-WATER-SPATIAL", "SPLASH4-WATER-NSQUARED"
        ],
        "NAS": [ #"bt.W.x",
            "bt.A.x", "cg.A.x", "cg.W.x",            
            "ep.A.x", "ep.W.x", 
            "ft.A.x", "ft.W.x", "is.A.x", "is.W.x", 
            "lu.A.x", "lu.W.x", "mg.A.x", "mg.W.x", 
            "sp.A.x", "sp.W.x", "ua.A.x", "ua.W.x",
        ],
    }
    return benchmarks.get(benchmark, [])

def process_benchmark(benchmark, gem5_path, base_output_dir, ckpt_base_dir, benchmark_base_dir, configs, num_ticks):
    """Process a single benchmark and submit jobs for its applications."""
    applications = get_applications_by_benchmark(benchmark)
    benchmark_dir = os.path.join(benchmark_base_dir, "Splash-4" if benchmark == "SPLASH" else "NPB3.3-SER")
    ckpt_path = os.path.join(ckpt_base_dir, "SPLASH4" if benchmark == "SPLASH" else "NPB3.3-SER")

    for config in configs:
        if config == "generalBigO3": iq_size = 900
        elif config == "generalSmallO3": iq_size = 96
        else: 
            raise ValueError(f"Unknown config: {config}")
        for app in applications:
            app_name = getSplashName(app) if benchmark == "SPLASH" else app
            app_dir = resolve_app_directory(benchmark_dir, app) if benchmark == "SPLASH" else benchmark_dir
            app_path = os.path.join(app_dir, app)

            for num_IQs in [#1, 
                            2, 4, 6, 8, 12
                            #2, 3, 5, 7
                            ]:
                entries_per_IQ = math.ceil(iq_size / num_IQs)
                output_dir = create_directory(
                    os.path.join(base_output_dir, benchmark, config, app_name, f"IQs_{num_IQs}"),
                    clean_if_exists=True)
                print(f"Running {app} with IQ size {iq_size}, num_IQs {num_IQs} on {config}")
                
                sbatch_script = generate_sbatch_script(
                    gem5_path, output_dir, config, iq_size, app_name, app_path, ckpt_path, num_ticks, num_IQs, entries_per_IQ)


                submit_job(sbatch_script)
                time.sleep(2)
               

def main(benchmark):
    """Main function to orchestrate the job submission."""
    print("Executing main")

    gem5_path = "/nfs/home/ce/alonsoge/gem5/"
    base_output_dir = "/nfs/home/ce/alonsoge/gem5/tfg/out/batch-Dividida-IQmax/"
    ckpt_base_dir = "/nfs/shared/ce/gem5/ckpts/x86/1core/1GB/"
    benchmark_base_dir = "/nfs/shared/ce/gem5/bin/"
    
    configs = [#"generalBigO3", 
               "generalSmallO3",
               ]
    benchmarks = [benchmark] if benchmark != "ALL" else ["SPLASH", "NAS"]
    num_ticks = 50000000000

    for bm in benchmarks:
        process_benchmark(bm, gem5_path, base_output_dir, ckpt_base_dir, benchmark_base_dir, configs, num_ticks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run gem5 simulations for NAS, SPLASH or all benchmarks.")
    parser.add_argument("benchmark", choices=["NAS", "SPLASH", "ALL"], help="Benchmark option to run.")
    args = parser.parse_args()

    main(args.benchmark)

