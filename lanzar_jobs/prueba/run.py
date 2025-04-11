import os
import re
import subprocess
import sys

import matplotlib.pyplot as plt

# Posibles tamaños de IQ
iq_sizes = ["16", "256", "1024"]
output_dir = "tfg/board/out/iq_sizes"

# Ejecutar el comando por cada tamaño de IQ
for iq_size in iq_sizes:
    command = [
        "build/X86/gem5.opt",
        "-re",
        f"--outdir={output_dir}/iq{iq_size}",
        "tfg/board/configs/configO3board.py",
        "--iq_size",
        iq_size,
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

# Extraer valores de IPC
ipc_values = []

for iq_size in iq_sizes:
    stats_file = f"{output_dir}/iq{iq_size}/stats.txt"

    if not os.path.exists(stats_file):
        print(f"Warning: stats file not found for IQ size {iq_size}")
        continue

    with open(stats_file) as file:
        for line in file:
            match = re.match(
                r"board\.processor\.cores\.core\.ipc\s+([\d.]+)", line
            )
            if match:
                ipc_values.append(float(match.group(1)))
                break

# Verificar que se obtuvieron todos los valores de IPC
if len(ipc_values) != len(iq_sizes):
    print("Error: No se pudieron obtener todos los valores de IPC.")
    sys.exit(1)

# Grafica con lps resultados
plt.figure(figsize=(8, 5))
plt.plot(
    [int(iq) for iq in iq_sizes],
    ipc_values,
    marker="o",
    linestyle="-",
    color="b",
    label="IPC",
)
plt.xlabel("IQ Size")
plt.ylabel("IPC")
plt.title("IQ Size vs IPC")
plt.grid(True)
plt.legend()
plt.savefig(f"{output_dir}/ipc_vs_iq.png")

print(f"Gráfica generada: {output_dir}/ipc_vs_iq.png")
