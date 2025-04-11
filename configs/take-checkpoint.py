# Copyright (c) 2023 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This gem5 script creates a simple board to save a checkpoint.
"""

import argparse
from pathlib import Path

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
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import (
    PrivateL1CacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import (
    BinaryResource,
    FileResource,
    obtain_resource,
)
from gem5.simulate.simulator import (
    ExitEvent,
    Simulator,
)
from gem5.utils.requires import requires

parser = argparse.ArgumentParser()

parser.add_argument(
    "--ckpt_path",
    type=str,
    required=False,
    default="/nfs/shared/ce/gem5/ckpts/x86",
    help="The directory to store the checkpoint.",
)
parser.add_argument(
    "--application",
    type=str,
    required=False,
    default="namd",
    help="Application to be run. Can be selected from SPEC or SPLASH with just the name. Check SPEC.py",
)
parser.add_argument(
    "--app_args",
    type=str,
    required=False,
    help="Application arguments. Do not use with SPEC",
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
args = parser.parse_args()
requires(isa_required=ISA.X86)

cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="16KiB", l1i_size="16KiB")

memory = SingleChannelDDR4_2400(size="%dGiB" % args.mem_size)

processor = SimpleProcessor(
    cpu_type=CPUTypes.ATOMIC, isa=ISA.X86, num_cores=args.num_cores
)

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

numcores = "%dcore" % args.num_cores
ckpt_path = Path(args.ckpt_path, numcores)
memsize = "%dGB" % args.mem_size
ckpt_path = Path(ckpt_path, memsize)

# Comprueba el tipo de aplicacion
isSPEC = 0
isSplash = 0
isNPB = 0
if "SPLASH4" in args.application:
    isSplash = 1
    ckpt_path = Path(ckpt_path, "SPLASH4")
elif "SPEC" in args.application:
    isSPEC = 1
    ckpt_path = Path(ckpt_path, "SPEC17")
elif "NPB3.3-SER" in args.application:
    isNPB = 1
    ckpt_path = Path(ckpt_path, "NPB3.3-SER")
else:
    ckpt_path = Path(ckpt_path, "OTHERS")

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
    binary_args = getSplashArgs(args.application)
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

board.set_se_binary_workload(
    binary=BinaryResource(
        local_path=binary_path.as_posix(),
    ),
    stdin_file=input,
    arguments=binary_args,
)


if isSPEC:
    ckpt_name = "ckpt-" + args.application.split(".")[-1]
elif isSplash:
    ckpt_name = "ckpt-" + getSplashName(args.application)
else:
    ckpt_name = "ckpt-" + args.application.split("/")[-1]

ckpt_path = Path(ckpt_path, ckpt_name)
print("Taking checkpoint called %s, from path %s" % (ckpt_name, ckpt_path))

def workbegin_handler():
    print("Taking checkpoint…")
    print("Resetting stats before taking checkpoint!")
    m5.stats.reset()
    sim.save_checkpoint(ckpt_path)
    print("Done taking checkpoint")
    yield True


def workend_handler():
    print("Workend")
    m5.debug.flags["ExecAll"].disable()
    yield False


sim = Simulator(
    board=board,
    full_system=False,
    on_exit_event={
        ExitEvent.WORKBEGIN: workbegin_handler(),
        ExitEvent.WORKEND: workend_handler(),
    },
)

print("Running the simulation")
sim.run()
print(
    "Exiting @ tick {} because {}.".format(
        sim.get_current_tick(), sim.get_last_exit_event_cause()
    )
)
print("Simulation Done")
