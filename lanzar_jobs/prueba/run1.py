import os
import subprocess
import sys

# Verificar si el directorio ~/gem5 existe
gem5_home = os.path.expanduser("~/gem5")
if not os.path.isdir(gem5_home):
    print("gem5 must be cloned into the home directory.")
    sys.exit(1)

# Verificar los parámetros: tamaño de IQ
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <IQ size>")
    sys.exit(1)

iq_size = sys.argv[1]

# Ejecutar el comando
command = [
    "build/X86/gem5.opt",
    "-re",
    f"--outdir=tfg/board/out/iq{iq_size}",
    "tfg/board/configs/configO3board.py",
    "--iq_size",
    iq_size,
]

try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    sys.exit(1)
