# Default argument values
DEFAULT_IQ_SIZE = 256
DEFAULT_CKPT_PATH = "~/x86-hello-test-checkpoint/"
DEFAULT_APPLICATION = "namd"
DEFAULT_WORKS = 1
DEFAULT_MEM_SIZE = "1GB"
DEFAULT_NUM_CORES = 1
DEFAULT_NUM_TICKS = 1000000000000

# Big O3 Processor configuration
BIG_O3_PROCESSOR_CONFIG = {
    "frontend_width": 10,
    "backend_width": 12,
    "rob_size": 900,             # Maximo, o sale:  Assertion `cpu->instcount <= 1500' failed. Original era 630.
    "lsq_size": 512,           
    "num_int_phys_regs": 916,    # Eran 630, pero pongo > rob_size para que no limite (mayoria de ejemplos pone de 16 a 64 mas)
    "num_fp_phys_regs": 932,
    "fu_pool": "Big",
    "bp": "PerceptBP",
    "numEntriesBtb": 2048 * 4,
    "tagBitsBtb": 18,
    "numEntriesRas": 48,
    "num_filter_entries": 0,
    "num_local_histories": 512,
    "local_history_length": 36,
}

# Small O3 Processor configuration
SMALL_O3_PROCESSOR_CONFIG = {
    "frontend_width": 3,
    "backend_width": 7,
    "rob_size": 96,
    "lsq_size": 48,               # Eran 36
    "num_int_phys_regs": 127,
    "num_fp_phys_regs": 119,
    "fu_pool": "Small",
    "bp": "TournBP",
    "numEntriesBtb": 32,
    "numEntriesRas": 15,
}

# Modular backend big O3 configuration, but different fu_pool
GENERAL_O3_PROCESSOR_CONFIG = {
    "frontend_width": 10,
    "backend_width": 12,
    "rob_size": 900,
    "lsq_size": 512,
    "num_int_phys_regs": 916,
    "num_fp_phys_regs": 932,
    "fu_pool": "General",
    "num_ports": 4,               # Sera un parametro luego
    "bp": "PerceptBP",
    "numEntriesBtb": 2048 * 4,
    "tagBitsBtb": 18,
    "numEntriesRas": 48,
    "num_filter_entries": 0,
    "num_local_histories": 512,
    "local_history_length": 36,
}

# Big O3 Cache hierarchy configuration
BIG_O3_CACHE_CONFIG = {
    "l1i_assoc": 8,
    "l1i_size": "32kB",
    "l1i_tag_latency": 1,
    "l1i_data_latency": 1,
    "l1i_response_latency": 1,
    "l1d_assoc": 8,
    "l1d_size": "32kB",
    "l1d_tag_latency": 1,
    "l1d_data_latency": 2,
    "l1d_response_latency": 1,
    "l1d_writeback_clean": False,
    "l2_assoc": 16,
    "l2_size": "1MB",
    "l2_tag_latency": 3,
    "l2_data_latency": 6,
    "l2_response_latency": 3,
    "l3_assoc": 16,
    "l3_size": "128MB",           # Eran 4MB originalmente
    "l3_tag_latency": 10,
    "l3_data_latency": 20,
    "l3_response_latency": 10,
}

# Small O3 Cache hierarchy configuration
SMALL_O3_CACHE_CONFIG = {
    "l1i_assoc": 4,
    "l1i_size": "32kB",
    "l1i_tag_latency": 1,
    "l1i_data_latency": 1,
    "l1i_response_latency": 1,
    "l1d_assoc": 4,
    "l1d_size": "32kB",
    "l1d_tag_latency": 1,
    "l1d_data_latency": 1,
    "l1d_response_latency": 1,
    "l1d_writeback_clean": True,
    "l2_assoc": 16,
    "l2_size": "256kB",
    "l2_tag_latency": 3,
    "l2_data_latency": 7,
    "l2_response_latency": 3,
    "l3_assoc": 16,
    "l3_size": "128MB",         # Eran 4MB originalmente
    "l3_tag_latency": 10,
    "l3_data_latency": 18,
    "l3_response_latency": 10,
}

# Big O3 Clock frequency
BIG_O3_CLOCK_FREQUENCY = "3GHz"

# Small O3 Clock frequency
SMALL_O3_CLOCK_FREQUENCY = "1.4GHz"
