import argparse
from componentsRiscv.customO3CPU import *
from componentsRiscv.customCacheHierarchy import *
from componentsRiscv.customFUPool import *

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import DualChannelDDR4_2400

# from gem5.resources.resource import BinaryResource
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# Argumentos
parser = argparse.ArgumentParser(
    description="Configuración de la simulación de gem5 con un procesador O3"
)
parser.add_argument(
    "--iq_size",
    type=int,
    default=104,
    help="Tamaño de la IQ del procesador O3",
)
args = parser.parse_args()

# Crea el procesador O3  TODO: revisar valores XT-910
ooo_processor = RiscvO3Processor(
    numCores=1,
    frontend_width=3,
    backend_width=8,
    dispatchWidth=4,
    renameWidth=4,
    commitWidth=3,
    rob_size=64,
    iq_size=args.iq_size,
    lsq_size=32,
    num_int_phys_regs=96,
    num_fp_phys_regs=64,
    fu_pool="Default",
    bp="TournBP",
    #TODO: cambiar BP numEntriesBHT=32768,
    numEntriesBtb=4096+16,
    numEntriesRas=12,
)

caches = ThreeLevelCacheHierarchy(
    # 64B line is the default value
    l1i_assoc=4,
    l1i_size="32kB",
    l1i_tag_latency=1,
    l1i_data_latency=1,
    l1i_response_latency=1,  # 3 cycle hit latency
    l1d_assoc=4,
    l1d_size="32kB",
    l1d_tag_latency=1,
    l1d_data_latency=1,
    l1d_response_latency=1,  # 4 cycle hit latency
    l1d_writeback_clean=True,
    l2_assoc=8,
    l2_size="256kB",
    l2_tag_latency=3,
    l2_data_latency=7,
    l2_response_latency=3,  # 13 cycle hit latency
    l3_assoc=16,
    l3_size="16MB",
    l3_tag_latency=10,
    l3_data_latency=18,
    l3_response_latency=10,  # 38 cycle hit latency
)

# Crea la memoria principal
main_memory = DualChannelDDR4_2400(size="4GB")

# Crea la placa base
board = SimpleBoard(
    clk_freq="1.3GHz", 
    memory=main_memory,
    cache_hierarchy=caches,
    processor=ooo_processor,
)

# Aplicaciones de gem5 resources:
workload = obtain_resource("riscv-npb-ft-size-s-run")
board.set_workload(workload)

# Lanza la simulacion
simulator = Simulator(board=board, full_system=False)
print("Empezando simulacion riscv!")
simulator.run()
print("Terminada la simulacion!")
