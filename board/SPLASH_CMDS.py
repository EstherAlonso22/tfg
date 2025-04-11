args_dict = {
    # APPS
    "OCEAN-CONT": "-p1 -n258",
    "OCEAN-NOCONT": "-p1 -n258",
    "RADIOSITY": "-p 1 -ae 5000 -bf 0.1 -en 0.05 -room –batch",
    "RAYTRACE": "-p1 -m64 inputs/car.env",
    "VOLREND": "1 inputs/head 8",
    "VOLREND-NPL": "1 inputs/head 8",

    # KERNELS
    "CHOLESKY": "-p1 inputs/tk15.O",
    "FFT": "-p1 -m16",
    "LU-CONT": "-p1 -n512",
    "LU-NOCONT": "-p1 -n512",
    "RADIX": "-p1 -n1048576",
}

inputs_dict = {
    # APPS
    "BARNES": "inputs/n16384-p1",
    "FMM": "inputs/input.1.16384",
    "WATER-NSQUARED": "inputs/n512-p1",
    "WATER-SPATIAL": "inputs/n512-p1",
}

app_dir_mapping = {
        "BARNES": "barnes",
        "CHOLESKY": "cholesky",
        "FFT": "fft",
        "FMM": "fmm",
        "LU-CONT": "lu-contiguous_blocks",
        "LU-NOCONT": "lu-non_contiguous_blocks",
        "OCEAN-CONT": "ocean-contiguous_partitions",
        "OCEAN-NOCONT": "ocean-non_contiguous_partitions",
        "RADIOSITY": "radiosity",
        "RADIX": "radix",
        "RAYTRACE": "raytrace",
        "VOLREND": "volrend",
        "VOLREND-NPL": "volrend-no_print_lock",
        "WATER-NSQUARED": "water-nsquared",
        "WATER-SPATIAL": "water-spatial",
    }
