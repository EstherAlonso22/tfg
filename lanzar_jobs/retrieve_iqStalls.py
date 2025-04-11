#!/usr/bin/env python3
import argparse
import os
import pandas as pd # type: ignore
import re

def extract_iqStalls(stats_file):
    try:
        with open(stats_file, "r") as f:
            for line in f:
                if "board.processor.cores.core.iew.iqFullEvents" in line:
                    return float(line.split()[1])  # Extract the second column as the IQ Stalls value
    except Exception as e:
        print(f"Error reading {stats_file}: {e}")
    return None

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
        "NAS": [
            "bt.A.x", "bt.W.x", "cg.A.x", "cg.W.x",            
            "ep.A.x", "ep.W.x", 
            "ft.A.x", "ft.W.x", "is.A.x", "is.W.x", 
            "lu.A.x", "lu.W.x", "mg.A.x", "mg.W.x", 
            "sp.A.x", "sp.W.x", "ua.A.x", "ua.W.x",
        ],
        "SPEC": [
            "cactuBSSN", "gcc", "lbm", "mcf", "namd", "povray", "x264", "xalan"
        ]
    }
    return benchmarks.get(benchmark, [])

def main(benchmark):
    print("Leyendo resultados")

    base_output_dir = f"/nfs/home/ce/alonsoge/gem5/tfg/board/out/batch/"
    if not os.path.exists(base_output_dir):
        print(f"Error: The directory {base_output_dir} does not exist.")
        return

    configs = ["bigO3", "smallO3"]
    iq_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    benchmarks = [benchmark] if benchmark != "ALL" else ["SPLASH", "NAS"]

    for benchmark in benchmarks:
        applications = get_applications_by_benchmark(benchmark)
        for config in configs:        
            all_data = []  # Lista para almacenar los datos de todas las aplicaciones
            for app in applications:
                if benchmark == "SPLASH":
                    app_name = re.search(r'SPLASH4-(.+)$', app).group(1)
                else:
                    app_name = app
                numIQStalls_values = []
                for iq_size in iq_sizes:
                    stats_file = f"{base_output_dir}/{benchmark}/{config}/{app_name}/iq_{iq_size}/stats.txt"
                    if not os.path.exists(stats_file):
                        print(f"Warning: stats file {stats_file} not found for {app} with IQ size {iq_size}")
                        continue

                    iqStalls = extract_iqStalls(stats_file)
                    if iqStalls is not None:
                        numIQStalls_values.append(iqStalls)

                if len(numIQStalls_values) != len(iq_sizes):
                    print(f"Error: Could not retrieve all iqStalls values for {app} with {config} configuration.")
                    continue

                # Agregar los valores de IQ Stalls de la aplicación a la lista de datos
                all_data.append([app] + numIQStalls_values)

            # Crear un DataFrame con todas las aplicaciones y sus valores de IQ Stalls
            df = pd.DataFrame(all_data, columns=["App"] + iq_sizes)

            # Definir la ruta del archivo CSV de salida
            output_csv_file = os.path.join(os.getcwd(), f"iqStalls_results_{benchmark}_{config}.csv")

            # Sobrescribir el archivo CSV con los nuevos datos
            df.to_csv(output_csv_file, index=False)

            # Dar formato adecuado
            with open(output_csv_file, "r") as file:
                content = file.read().replace(",", ";")
            content = re.sub(r'(?<=\d)\.(?=\d)', ',', content)
            
            with open(output_csv_file, "w") as file:
                file.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve results for a specific benchmark and export IQ Stalls data to CSV.")
    parser.add_argument("benchmark", choices=["NAS", "SPEC", "SPLASH", "ALL"], help="Benchmark option to process.")
    args = parser.parse_args()

    main(args.benchmark)
