import argparse

from pathlib import Path
from components.customCacheHierarchy import *
from components.customFUPool import *
from components.customO3CPU import *

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import DualChannelDDR4_2400
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource

from gem5.utils.requires import requires
from gem5.simulate.simulator import (ExitEvent, Simulator)
from SPEC import getExec, getExecArgs
import m5
import m5.debug

# Argumentos
parser = argparse.ArgumentParser(
    description="Configuración de la simulación de gem5 con un procesador O3"
)
parser.add_argument(
    "--iq_size",
    type=int,
    default=256,
    help="Tamaño de la IQ del procesador O3",
)
parser.add_argument(
    "--ckpt_path",
    type=str,
    required=False,
    default="x86-hello-test-checkpoint/",
    help="The directory to store the checkpoint.",
)
parser.add_argument(
    "--application",
    type=str,
    required=False,
    default="namd",
    help="Application from SPEC to be run. Check SPEC.py",
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
    numCores=args.num_cores,
    frontend_width=10,
    backend_width=12,  # = iq_issue_width
    rob_size=2048,
    iq_size=args.iq_size,
    lsq_size=256,
    num_int_phys_regs=630,
    num_fp_phys_regs=630,
    fu_pool="Custom",  # Options: "Custom", "Default"
    bp="PerceptBP",  # Options: "TournBP", "PerceptBP", "Default"
    numEntriesBtb=2048 * 4,
    tagBitsBtb=18,
    numEntriesRas=48,
    num_filter_entries=0,
    num_local_histories=512,
    local_history_length=36,
    globalPredictorSize=512,
)

caches = ThreeLevelCacheHierarchy(
    # 64B line is the default value
    l1i_assoc=8,
    l1i_size="32kB",
    l1i_tag_latency=1,
    l1i_data_latency=1,
    l1i_response_latency=1,  # 3 cycle hit latency
    l1d_assoc=8,
    l1d_size="32kB",
    l1d_tag_latency=1,
    l1d_data_latency=2,
    l1d_response_latency=1,  # 4 cycle hit latency
    l2_assoc=16,
    l2_size="1MB",
    l2_tag_latency=3,
    l2_data_latency=6,
    l2_response_latency=3,  # 12 cycle hit latency
    l3_assoc=16,
    l3_size="4MB",
    l3_tag_latency=10,
    l3_data_latency=20,
    l3_response_latency=10,  # 40 cycle hit latency
)

# Crea la memoria principal
main_memory = DualChannelDDR4_2400(size="%dGB" % args.mem_size)

# TODO: revisar si vale SimpleBoard o necesita X86Board
board = SimpleBoard(
    clk_freq="3GHz",
    memory=main_memory,
    cache_hierarchy=caches,
    processor=ooo_processor,
)

isSPEC = 0

if args.application.startswith("SPEC"):
    # SPEC
    isSPEC = 1
    binary_path = Path(getExec(args.application.split(".")[-1]))
else:
    binary_path = Path(args.application)

if binary_path.exists() != True:
    print("ERROR %s does not exist" % binary_path)
    exit()
else:
    print("Executing %s app" % binary_path)

if isSPEC:
    # SPEC
    binary_args = getExecArgs(args.application, args.app_args)
else:
    binary_args = args.app_args.split() if args.app_args else []

if isSPEC:
    ckpt_name = "ckpt-" + args.application.split(".")[-1]
else:
    ckpt_name = "ckpt-" + args.application.split("/")[-1]

ckpt_path = Path(args.ckpt_path, ckpt_name)


board.set_se_binary_workload(
    binary=BinaryResource(
        local_path=binary_path.as_posix(),
    ),
    arguments=binary_args,
    checkpoint=ckpt_path,
)

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
            print("Dumping stats before exiting")
            m5.stats.dump()
            yield True


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
