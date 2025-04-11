import argparse
from pathlib import Path

from components.customCacheHierarchy import *
from components.customFUPool import *
from components.customO3CPU import *
from SPEC import (
    getExec,
    getExecArgs,
)
from SPLASH import (
    getSplashName,
    getSplashArgs,
    getSplashInput,
)
import m5
import m5.debug

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import DualChannelDDR4_2400
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource, FileResource
from gem5.simulate.simulator import (
    ExitEvent,
    Simulator,
)
from gem5.utils.requires import requires

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
parser.add_argument(
    "--ckpt_path",
    type=str,
    required=False,
    default="~/x86-hello-test-checkpoint/",
    help="The directory to store the checkpoint.",
)
parser.add_argument(
    "--application",
    type=str,
    required=False,
    default="namd",
    help="Application from SPEC or SPLASH to be run. Check SPEC.py",
)
parser.add_argument(
    "--app_args",
    type=str,
    required=False,
    help="Application arguments. Do not use with SPEC",
)
parser.add_argument(
    "--works",
    type=str,
    required=False,
    default=1,
    help="Number of works until exit",
)
parser.add_argument(
    "--mem_size",
    type=int,
    required=False,
    default=1,
    help="Number of GB of Main memory for the checkpoint",
)
parser.add_argument(
    "--num_cores",
    type=int,
    required=False,
    default=1,
    help="Number of cores on the system for the checkpoint",
)
parser.add_argument(
    "--num_ticks",
    type=int,
    required=False,
    default=1000000000000,
    help="Number of ticks to run until simulation ends",
)
args = parser.parse_args()
requires(isa_required=ISA.X86)

# Crea el procesador O3
ooo_processor = O3Processor(
    numCores=1,
    frontend_width=3,
    backend_width=7, 
    rob_size=1400,
    iq_size=args.iq_size,
    lsq_size=36,
    num_int_phys_regs=1216,
    num_fp_phys_regs=1232,
    fu_pool="Small",  # Options: "Big", "Small", "Default"
    bp="TournBP",  # Options: "TournBP", "PerceptBP", "Default"
    numEntriesBtb=32,
    numEntriesRas=15, 
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
    l2_assoc=16,
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
main_memory = DualChannelDDR4_2400(size="%dGB" % args.mem_size)

# Crea la board
board = SimpleBoard(
    clk_freq="1.4GHz",
    memory=main_memory,
    cache_hierarchy=caches,
    processor=ooo_processor,
)

# Comprueba el tipo de aplicacion
isSPEC = 0
isSplash = 0
if "SPLASH4" in args.application:
    isSplash = 1
elif args.application.startswith("SPEC"):
    isSPEC = 1

# Path a la aplicacion
if isSPEC:
    binary_path = Path(getExec(args.application.split(".")[-1]))
else:
    binary_path = Path(args.application)

if binary_path.exists() != True:
    print("ERROR %s does not exist" % binary_path)
    exit()
else:
    print("Executing %s app" % binary_path)

# Argumentos de la aplicacion
if isSPEC:
    binary_args = getExecArgs(args.application.split(".")[-1], 1)
    input = None
elif isSplash: 
    splash_args = getSplashArgs(args.application)
    binary_args = splash_args.split() if splash_args else []
    input = getSplashInput(args.application)
    if input:
        input_path = Path(input)
        if input_path.exists() != True:
            print("ERROR %s does not exist" % input_path)
            exit()
        input = FileResource(local_path=input_path.as_posix())
else:
    binary_args = args.app_args.split() if args.app_args else []
    input = None

# Path al checkpoint a restaurar
if isSPEC:
    ckpt_name = "ckpt-" + args.application.split(".")[-1]
elif isSplash:
    ckpt_name = "ckpt-" + getSplashName(args.application)
else:
    ckpt_name = "ckpt-" + args.application.split("/")[-1]
ckpt_path = Path(args.ckpt_path, ckpt_name)

# Configura la aplicacion
board.set_se_binary_workload(
    binary=BinaryResource(
        local_path=binary_path.as_posix(),
    ),
    arguments=binary_args,
    stdin_file=input,
    checkpoint=ckpt_path,
)

# Funcion para ejecutar el numero de works especificado
num_works = 0

def workend_handler():
    while True:
        global num_works
        num_works = num_works + 1
        print("Workend %d" % num_works)
        m5.debug.flags["ExecAll"].disable()
        if num_works < int(args.works):
            yield False
        else:
            yield True

# Lanza la simulacion
sim = Simulator(
    board=board,
    full_system=False,
    on_exit_event={ExitEvent.WORKEND: workend_handler()},
)
sim.run(args.num_ticks)

print(
    "Exiting @ tick {} because {}.".format(
        sim.get_current_tick(), sim.get_last_exit_event_cause()
    )
)