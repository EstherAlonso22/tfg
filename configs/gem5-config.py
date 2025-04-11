import argparse

from components.customCacheHierarchy import *
from components.customFUPool import *
from components.customO3CPU import *

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import DualChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

from data import (
    DEFAULT_IQ_SIZE,
    DEFAULT_MEM_SIZE,
    DEFAULT_NUM_CORES,
    BIG_O3_PROCESSOR_CONFIG,
    SMALL_O3_PROCESSOR_CONFIG,
    GENERAL_O3_PROCESSOR_CONFIG,
    BIG_O3_CACHE_CONFIG,
    SMALL_O3_CACHE_CONFIG,
    BIG_O3_CLOCK_FREQUENCY,
    SMALL_O3_CLOCK_FREQUENCY,
)

# Argumentos
parser = argparse.ArgumentParser(
    description="Configuración genérica de la simulación de gem5"
)
parser.add_argument(
    "--iq_size",
    type=int,
    default=DEFAULT_IQ_SIZE,
    help="Tamaño de la IQ del procesador O3",
)
parser.add_argument(
    "--config",
    type=str,
    choices=["bigO3", "smallO3", "generalO3"],
    default="bigO3",
    help="Select the processor configuration: bigO3, smallO3, or generalO3(generic ports)",
)
args = parser.parse_args()

# Configuración del procesador O3
if args.config == "bigO3":
    processor_config = BIG_O3_PROCESSOR_CONFIG
elif args.config == "smallO3":
    processor_config = SMALL_O3_PROCESSOR_CONFIG
elif args.config == "generalO3":
    processor_config = GENERAL_O3_PROCESSOR_CONFIG

ooo_processor = O3Processor(
    numCores=DEFAULT_NUM_CORES,
    iq_size=args.iq_size,
    **processor_config,
)

# Configuración de la jerarquia de cache
cache_config = (
    SMALL_O3_CACHE_CONFIG if args.config == "smallO3" else BIG_O3_CACHE_CONFIG
)
caches = ThreeLevelCacheHierarchy(**cache_config)

# Configuración de la memoria principal
main_memory = DualChannelDDR4_2400(size=DEFAULT_MEM_SIZE)

# Configuración de la board
board = SimpleBoard(
    clk_freq=SMALL_O3_CLOCK_FREQUENCY if args.config == "smallO3" else BIG_O3_CLOCK_FREQUENCY,
    memory=main_memory,
    cache_hierarchy=caches,
    processor=ooo_processor,
)

# Asigna programa a ejecutar
workload = obtain_resource("x86-npb-is-size-s-run")
board.set_workload(workload)

# Lanza la simulación
simulator = Simulator(board=board, full_system=False)
print("Empezando simulación!")
simulator.run()
print("Terminada la simulación!")
