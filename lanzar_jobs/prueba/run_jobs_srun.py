import os
import subprocess

def create_output_dirs(base_dir, config, iq_size, app_name):
    output_dir = os.path.join(base_dir, config, app_name, f"iq_{iq_size}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def submit_job(output_dir, config, iq_size, app_path, ckpt_path, app_args):
    command = [
        "srun", 
        "--partition=ce_100",
        "build/X86/gem5.opt",
        f"--outdir={output_dir}",
        f"tfg/board/configs/{config}-restore-checkpoint-splash.py",
        "--ckpt_path", ckpt_path,
        "--application", app_path,
        "--num_cores", "1",
        "--mem_size", "1",
        "--app_args", app_args,
        "--works", "2",
        "--num_ticks", "100000000",
        "--iq_size", str(iq_size)
    ]
    subprocess.run(command)

def main():
    os.chdir(os.path.expanduser("~/gem5"))
    print(f"Directorio actual: {os.getcwd()}") 

    base_output_dir = "tfg/board/out/batch"
    ckpt_path = "/nfs/shared/ce/gem5/ckpts/x86/1core/1GB"
    apps_base_dir = "/nfs/shared/ce/gem5/bin/Splash-4/fft"
    
    configs = ["bigO3"]
    iq_sizes = [32, 256] 
    applications = ["SPLASH4-FFT"] # TODO: poner aplicaciones y argumentos (dict)
    app_args = "-p1 -n1048576"
    for config in configs:
        for app in applications:
            app_path = os.path.join(apps_base_dir, app)
            for iq_size in iq_sizes:
                output_dir = create_output_dirs(base_output_dir, config, iq_size, app)
                submit_job(output_dir, config, iq_size, app_path, ckpt_path, app_args)

if __name__ == "__main__":
    main()