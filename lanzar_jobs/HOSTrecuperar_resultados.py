#!/usr/bin/env python3
#Solo añadido aqui para guardarlo en el repo, se ejecuta desde el host para recuperar los resultados del cpd y hacer las graficas
import os
import pandas as pd
import paramiko
from paramiko import RSAKey, DSSKey, ECDSAKey, Ed25519Key
from paramiko.ssh_exception import PasswordRequiredException, SSHException
from scp import SCPClient
from pathlib import Path

# Configuración de conexión
remote_host = 'calderon.sci.unican.es'
remote_user = 'alonsoge'
ssh_key_path = '~/.ssh/id_ed25519-ui'
remote_path = '/nfs/home/ce/alonsoge/gem5/tfg/lanzar_jobs/'
local_path = '.'
excel_output = 'resultados_completos.xlsx'

def load_ssh_key(path, password):
    for key_class in [Ed25519Key, ECDSAKey, RSAKey, DSSKey]:
        try:
            return key_class.from_private_key_file(path, password=password)
        except (PasswordRequiredException, SSHException):
            continue
    raise ValueError("No se pudo cargar la clave privada con ninguna clase compatible.")

# Crear cliente SSH
def create_ssh_client():
    from getpass import getpass
    key_password = getpass("Introduce la contraseña de la clave privada SSH: ")
    key = load_ssh_key(os.path.expanduser(ssh_key_path), key_password)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(remote_host, username=remote_user, pkey=key)
    return client

# Descargar archivos CSV
def download_files():
    os.makedirs(local_path, exist_ok=True)
    ssh = create_ssh_client()
    with SCPClient(ssh.get_transport()) as scp:
        stdin, stdout, stderr = ssh.exec_command(f'ls {remote_path}*_results_*.csv')
        files = stdout.read().decode().split()
        for file in files:
            scp.get(file, local_path)
    ssh.close()

# Convertir y cargar CSVs
def process_csv_files():
    excel_writer = pd.ExcelWriter(excel_output, engine='xlsxwriter')
    grouped_data = {}

    # Preparar datos para el gráfico de resumen
    summary_data = []

    # Agrupar los CSV por benchmark+config
    for csv_file in Path(local_path).glob("*_results_*.csv"):
        result_type, _, benchmark, config = csv_file.stem.split("_")
        df = pd.read_csv(csv_file, sep=';', decimal=',')

        sheet_name = f"{benchmark}_{config}"
        if sheet_name not in grouped_data:
            grouped_data[sheet_name] = {}
        grouped_data[sheet_name][result_type] = df

    # Para cada grupo, crear hoja y gráficos
    for sheet, results in grouped_data.items():
        workbook = excel_writer.book
        worksheet = workbook.add_worksheet(sheet)
        excel_writer.sheets[sheet] = worksheet

        row_offset = 0

        # Generar gráficos en orden: primero IPC, luego IQ stalls
        for result_type in ['ipc', 'iqStalls']:
            if result_type not in results:
                continue

            df = results[result_type]
            # Calcular la media
            df_mean = pd.DataFrame([["MEDIA"] + df.iloc[:, 1:].mean().tolist()], columns=df.columns)
            df = pd.concat([df, df_mean], ignore_index=True)

            # Guardar las medias en summary_data
            if result_type == 'ipc':
                summary_data.append((sheet, df_mean.iloc[0, 1:].tolist()))

            # Escribir la tabla
            df.to_excel(excel_writer, sheet_name=sheet, startrow=row_offset, startcol=0, index=False, header=True)

            # Crear gráfico
            chart = workbook.add_chart({'type': 'line'})
            iq_count = df.shape[1] - 1  # columnas de IQ
            num_rows = df.shape[0] - 1  # sin la fila header

            for i in range(num_rows):  # sin incluir la MEDIA
                chart.add_series({
                    'name':       [sheet, row_offset + i + 1, 0],
                    'categories': [sheet, row_offset, 1, row_offset, iq_count],
                    'values':     [sheet, row_offset + i + 1, 1, row_offset + i + 1, iq_count],
                    'line':       {'width': 1.5},
                    'marker':     {'type': 'circle', 'size': 4},
                    
                })

            # MEDIA → rosa fucsia, discontinua
            chart.add_series({
                'name':       'MEDIA',
                'categories': [sheet, row_offset, 1, row_offset, iq_count],
                'values':     [sheet, row_offset + num_rows + 1, 1, row_offset + num_rows + 1, iq_count],
                'line': {
                    'color': '#FF00FF',
                    'dash_type': 'dash',
                    'width': 2.25
                },
                'marker': {'type': 'circle', 'size': 6,  'fill': {'color': '#FF00FF'}, 'border': {'color': '#FF00FF'}}
            })

            chart.set_title({'name': f"{result_type.upper()} - {sheet}"})
            chart.set_x_axis({'name': 'Tamaño IQ'})
            chart.set_y_axis({'name': result_type.upper()})
            chart.set_legend({'position': 'right'})

            # Hacer el gráfico más grande
            chart.set_size({'width': 960, 'height': 540})

            # Insertar el gráfico al lado derecho de la tabla
            worksheet.insert_chart(row_offset, iq_count + 3, chart)

            row_offset += df.shape[0] + 6  # espacio entre tablas

    # Crear hoja y gráfico de resumen de medias de IPC
    summary_sheet_name = "Resumen_IPC"
    workbook = excel_writer.book
    worksheet = workbook.add_worksheet(summary_sheet_name)
    excel_writer.sheets[summary_sheet_name] = worksheet

    # Escribir encabezado de la hoja de resumen
    iq_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    worksheet.write(0, 0, "Benchmark-Config")
    for col_offset, iq_size in enumerate(iq_sizes, start=1):
        worksheet.write(0, col_offset, iq_size)

    # Escribir datos en la hoja de resumen
    row_offset = 1
    for sheet_name, media_row in summary_data:
        worksheet.write(row_offset, 0, sheet_name)
        for col_offset, value in enumerate(media_row, start=1):
            worksheet.write(row_offset, col_offset, value)
        row_offset += 1

    # Crear gráfico de resumen
    chart = workbook.add_chart({'type': 'line'})
    for row in range(1, row_offset):
        chart.add_series({
            'name':       [summary_sheet_name, row, 0],
            'categories': [summary_sheet_name, 0, 1, 0, len(iq_sizes)],
            'values':     [summary_sheet_name, row, 1, row, len(iq_sizes)],
            'line':       {'marker': 'circle'},
            'marker':     {'type': 'circle', 'size': 6},
            'width': 1.5
        })

    chart.set_title({'name': 'Resumen de IPC - Media'})
    chart.set_x_axis({'name': 'Tamaño IQ', 'categories': iq_sizes})
    chart.set_y_axis({'name': 'IPC'})
    chart.set_legend({'position': 'right'})

    # Hacer el gráfico más grande
    chart.set_size({'width': 960, 'height': 540})

    # Insertar el gráfico en la hoja de resumen
    worksheet.insert_chart(1, len(iq_sizes) + 2, chart)

    excel_writer.close()

# Ejecutar todo
#download_files()
process_csv_files()
print(f"✅ Resultados y gráficas generadas en '{excel_output}'")