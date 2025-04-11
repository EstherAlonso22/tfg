import argparse
from pathlib import Path

from components.customCacheHierarchy import *
from components.customFUPool import *
from components.customO3CPU import *
from SPEC import getExec, getExecArgs
from SPLASH import getSplashName, getSplashArgs, getSplashInput
import m5
import m5.debug

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import DualChannelDDR4_2400
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource, FileResource
from gem5.simulate.simulator import ExitEvent, Simulator
from gem5.utils.requires import requires

from data import (
    DEFAULT_IQ_SIZE,
    DEFAULT_CKPT_PATH,
    DEFAULT_APPLICATION,
    DEFAULT_WORKS,
    DEFAULT_MEM_SIZE,
    DEFAULT_NUM_CORES,
    DEFAULT_NUM_TICKS,
    BIG_O3_PROCESSOR_CONFIG,
    SMALL_O3_PROCESSOR_CONFIG,
    GENERAL_O3_PROCESSOR_CONFIG,
    BIG_O3_CACHE_CONFIG,
    SMALL_O3_CACHE_CONFIG,
    BIG_O3_CLOCK_FREQUENCY,
    SMALL_O3_CLOCK_FREQUENCY,
)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Configuración de la simulación de gem5 con un procesador O3"
    )
    parser.add_argument("--config", type=str, choices=["bigO3", "smallO3", "generalO3"], default="bigO3", help="Select the processor configuration: bigO3, smallO3, or generalO3(generic ports)")
    parser.add_argument("--iq_size", type=int, default=DEFAULT_IQ_SIZE, help="Tamaño de la IQ del procesador O3")
    parser.add_argument("--ckpt_path", type=str, default=DEFAULT_CKPT_PATH, help="The directory to store the checkpoint.")
    parser.add_argument("--application", type=str, default=DEFAULT_APPLICATION, help="Application from SPEC or SPLASH to be run. Check SPEC.py")
    parser.add_argument("--app_args", type=str, help="Application arguments. Do not use with SPEC")
    parser.add_argument("--works", type=str, default=DEFAULT_WORKS, help="Number of works until exit")
    parser.add_argument("--mem_size", type=int, default=DEFAULT_MEM_SIZE, help="Number of GB of Main memory for the checkpoint")
    parser.add_argument("--num_cores", type=int, default=DEFAULT_NUM_CORES, help="Number of cores on the system for the checkpoint")
    parser.add_argument("--num_ticks", type=int, default=DEFAULT_NUM_TICKS, help="Number of ticks to run until simulation ends")
    return parser.parse_args()

def create_processor(args):
    if args.config == "bigO3":
        processor_config = BIG_O3_PROCESSOR_CONFIG
    elif args.config == "smallO3":
        processor_config = SMALL_O3_PROCESSOR_CONFIG
    elif args.config == "generalO3":
        processor_config = GENERAL_O3_PROCESSOR_CONFIG
    return O3Processor(
        numCores=args.num_cores,
        **processor_config,
        iq_size=args.iq_size,
    )

def create_cache_hierarchy(args):
    cache_config = SMALL_O3_CACHE_CONFIG if args.config == "smallO3" else BIG_O3_CACHE_CONFIG
    return ThreeLevelCacheHierarchy(**cache_config)

def get_clock_frequency(args):
    return SMALL_O3_CLOCK_FREQUENCY if args.config == "smallO3" else BIG_O3_CLOCK_FREQUENCY

def get_binary_and_args(args):
    isSPEC = "SPEC" in args.application
    isSplash = "SPLASH4" in args.application

    if isSPEC:
        binary_path = Path(getExec(args.application.split(".")[-1]))
        binary_args = getExecArgs(args.application.split(".")[-1], 1)
        input_file = None
    elif isSplash:
        binary_path = Path(args.application)
        splash_args = getSplashArgs(args.application)
        binary_args = splash_args.split() if splash_args else []
        input_file = getSplashInput(args.application)
        if input_file:
            input_path = Path(input_file)
            if not input_path.exists():
                raise FileNotFoundError(f"ERROR {input_path} does not exist")
            input_file = FileResource(local_path=input_path.as_posix())
    else:
        binary_path = Path(args.application)
        binary_args = args.app_args.split() if args.app_args else []
        input_file = None

    if not binary_path.exists():
        raise FileNotFoundError(f"ERROR {binary_path} does not exist")

    return binary_path, binary_args, input_file

def get_checkpoint_path(args):
    if "SPEC" in args.application:
        ckpt_name = f"ckpt-{args.application.split('.')[-1]}"
    elif "SPLASH4" in args.application:
        ckpt_name = f"ckpt-{getSplashName(args.application)}"
    else:
        ckpt_name = f"ckpt-{args.application.split('/')[-1]}"
    return Path(args.ckpt_path, ckpt_name)

def workend_handler(args):
    num_works = 0
    while True:
        num_works += 1
        print(f"Workend {num_works}")
        m5.debug.flags["ExecAll"].disable()
        if num_works < int(args.works):
            yield False
        else:
            yield True

# Main gem5 simulation script
args = parse_arguments()
requires(isa_required=ISA.X86)

processor = create_processor(args)

caches = create_cache_hierarchy(args)
main_memory = DualChannelDDR4_2400(size=f"{args.mem_size}GB")
clock_frequency = get_clock_frequency(args)

board = SimpleBoard(clk_freq=clock_frequency, memory=main_memory, cache_hierarchy=caches, processor=processor)

binary_path, binary_args, input_file = get_binary_and_args(args)
ckpt_path = get_checkpoint_path(args)
board.set_se_binary_workload(
    binary=BinaryResource(local_path=binary_path.as_posix()),
    arguments=binary_args,
    stdin_file=input_file,
    checkpoint=ckpt_path,
)
sim = Simulator(
    board=board,
    full_system=False,
    on_exit_event={ExitEvent.WORKEND: workend_handler(args)},
)
sim.run(args.num_ticks)

print(f"Exiting @ tick {sim.get_current_tick()} because {sim.get_last_exit_event_cause()}.")


