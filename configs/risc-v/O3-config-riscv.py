import argparse
from componentsRiscv.customO3CPU import *
from componentsRiscv.customCacheHierarchy import *
from componentsRiscv.customFUPool import *

from gem5.components.boards.simple_board import SimpleBoard
#from m5.objects.SimpleMemory import SimpleMemory
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
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
    fetchWidth=8,
    dispatchWidth=4,
    renameWidth=4,
    commitWidth=3,
    issueWidth=3,
    rob_size=64,
    iq_size=args.iq_size,
    lq_entries=16,
    sq_entries=12,
    num_int_phys_regs=96,
    num_fp_phys_regs=64,
    fu_pool="Default",
    bp="TAGE_BP"
)

caches = PrivateL1SharedL2CacheHierarchy(
    # 64B line is the default value
    l1i_assoc=2,
    l1i_size="64kB",    
    l1d_assoc=2,
    l1d_size="64kB",
    l2_assoc=8,
    l2_size="128kB",
)

# Crea la memoria principal
#TODO: cambiar a memoria ideal. 
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
