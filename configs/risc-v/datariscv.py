# Default argument values
DEFAULT_CKPT_PATH = "~/ckpts/"
DEFAULT_APPLICATION = "prueba"
DEFAULT_WORKS = 1
DEFAULT_MEM_SIZE = 1
DEFAULT_NUM_CORES = 1
DEFAULT_NUM_TICKS = 1000000000

# RISC-V O3 Processor configuration (C910)
RISCV_O3_PROCESSOR_CONFIG = {
    "frontend_width": 3,
    "backend_width": 8,
    "rob_size": 64,
    "iq_size": 64,
    "lq_entries": 16,
    "sq_entries": 12,
    "num_int_phys_regs": 96,
    "num_fp_phys_regs": 64,
    "fu_pool": "Default",
    "bp": "TAGE_BP"
}

# O3 Cache hierarchy configuration (C910)
RISCV_O3_CACHE_CONFIG = {
    "l1i_assoc": 2,
    "l1i_size": "64kB",    
    "l1d_assoc": 2,
    "l1d_size": "64kB",
    "l2_assoc": 8,
    "l2_size": "128kB"
}

# O3 Clock frequency (C910)
RISCV_O3_CLOCK_FREQUENCY = "1.3GHz"

