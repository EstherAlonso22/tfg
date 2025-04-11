"""
This module contains a three-level cache hierarchy with private L1 caches,
private L2 caches, and a shared L3 cache.
"""

# from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache
# from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
# from gem5.components.cachehierarchies.classic.caches.l2cache import L2Cache
from components.customCaches import (
    L1DCache,
    L1ICache,
    L2Cache,
    L3Cache,
)

from m5.objects import (
    BadAddr,
    Cache,
    L2XBar,
    SubSystem,
    SystemXBar,
)

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)
from gem5.components.cachehierarchies.classic.caches.mmu_cache import MMUCache
from gem5.isas import ISA


class ThreeLevelCacheHierarchy(AbstractClassicCacheHierarchy):
    def __init__(
        self,
        l1i_assoc,
        l1i_size,
        l1i_tag_latency,
        l1i_data_latency,
        l1i_response_latency,
        l1d_assoc,
        l1d_size,
        l1d_tag_latency,
        l1d_data_latency,
        l1d_response_latency,
        l1d_writeback_clean,
        l2_assoc,
        l2_size,
        l2_tag_latency,
        l2_data_latency,
        l2_response_latency,
        l3_assoc,
        l3_size,
        l3_tag_latency,
        l3_data_latency,
        l3_response_latency,
    ):
        AbstractClassicCacheHierarchy.__init__(self)

        # Save the sizes and latencies to use later.
        self._l1i_size = l1i_size
        self._l1i_assoc = l1i_assoc
        self._l1i_tag_latency = l1i_tag_latency
        self._l1i_data_latency = l1i_data_latency
        self._l1i_response_latency = l1i_response_latency

        self._l1d_size = l1d_size
        self._l1d_assoc = l1d_assoc
        self._l1d_tag_latency = l1d_tag_latency
        self._l1d_data_latency = l1d_data_latency
        self._l1d_response_latency = l1d_response_latency
        self._l1d_writeback_clean = l1d_writeback_clean

        self._l2_size = l2_size
        self._l2_assoc = l2_assoc
        self._l2_tag_latency = l2_tag_latency
        self._l2_data_latency = l2_data_latency
        self._l2_response_latency = l2_response_latency

        self._l3_size = l3_size
        self._l3_assoc = l3_assoc
        self._l3_tag_latency = l3_tag_latency
        self._l3_data_latency = l3_data_latency
        self._l3_response_latency = l3_response_latency

        # Use a high-bandwidth system crossbar.
        self.membus = SystemXBar(width=64)
        # For FS mode
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio

    # To connect the memory system to the caches
    def get_mem_side_port(self):
        return self.membus.mem_side_ports

    # For FS mode. This is a coherent port.
    def get_cpu_side_port(self):
        return self.membus.cpu_side_ports

    # This is where the bulk of the work happens.
    # The board calls this function after it has created the processor and
    # memory system. The cache hierarchy is responsible for connecting things.
    def incorporate_cache(self, board):
        # Connect the system port to the memory system.
        board.connect_system_port(self.membus.cpu_side_ports)

        # Connect the memory system to the memory port on the board.
        for _, port in board.get_memory().get_mem_ports():
            self.membus.mem_side_ports = port

        # Create an L3 crossbar
        self.l3_bus = L2XBar()

        self.clusters = [
            self._create_core_cluster(
                core, self.l3_bus, board.get_processor().get_isa()
            )
            for core in board.get_processor().get_cores()
        ]

        self.l3_cache = L3Cache(
            size=self._l3_size,
            assoc=self._l3_assoc,
            tag_latency=self._l3_tag_latency,
            data_latency=self._l3_data_latency,
            response_latency=self._l3_response_latency,
        )

        # Connect the L3 cache to the system crossbar and L3 crossbar
        self.l3_cache.mem_side = self.membus.cpu_side_ports
        self.l3_cache.cpu_side = self.l3_bus.mem_side_ports

        # Give option to connect a cache for coherent I/O
        if board.has_coherent_io():
            self._setup_io_cache(board)

    def _create_core_cluster(self, core, l3_bus, isa):
        """
        Create a core cluster with the given core.
        """
        cluster = SubSystem()
        cluster.l1dcache = L1DCache(
            size=self._l1d_size,
            assoc=self._l1d_assoc,
            tag_latency=self._l1d_tag_latency,
            data_latency=self._l1d_data_latency,
            response_latency=self._l1d_response_latency,
            writeback_clean=self._l1d_writeback_clean,

        )
        cluster.l1icache = L1ICache(
            size=self._l1i_size,
            assoc=self._l1i_assoc,
            tag_latency=self._l1i_tag_latency,
            data_latency=self._l1i_data_latency,
            response_latency=self._l1i_response_latency,
        )
        cluster.l2cache = L2Cache(
            size=self._l2_size,
            assoc=self._l2_assoc,
            tag_latency=self._l2_tag_latency,
            data_latency=self._l2_data_latency,
            response_latency=self._l2_response_latency,
        )

        cluster.iptw_cache = MMUCache(size="8KiB", writeback_clean=False)
        cluster.dptw_cache = MMUCache(size="8KiB", writeback_clean=False)

        cluster.l2_bus = L2XBar()

        # Connect the core to the caches
        core.connect_icache(cluster.l1icache.cpu_side)
        core.connect_dcache(cluster.l1dcache.cpu_side)
        core.connect_walker_ports(
            cluster.iptw_cache.cpu_side, cluster.dptw_cache.cpu_side
        )

        # Connect the caches to the L2 bus
        cluster.l1dcache.mem_side = cluster.l2_bus.cpu_side_ports
        cluster.l1icache.mem_side = cluster.l2_bus.cpu_side_ports
        cluster.iptw_cache.mem_side = cluster.l2_bus.cpu_side_ports
        cluster.dptw_cache.mem_side = cluster.l2_bus.cpu_side_ports

        cluster.l2cache.cpu_side = cluster.l2_bus.mem_side_ports

        cluster.l2cache.mem_side = l3_bus.cpu_side_ports

        if isa == ISA.X86:
            int_req_port = self.membus.mem_side_ports
            int_resp_port = self.membus.cpu_side_ports
            core.connect_interrupt(int_req_port, int_resp_port)
        else:
            core.connect_interrupt()

        return cluster

    def _setup_io_cache(self, board: AbstractBoard) -> None:
        """Create a cache for coherent I/O connections"""
        self.iocache = Cache(
            assoc=8,
            tag_latency=50,
            data_latency=50,
            response_latency=50,
            mshrs=20,
            size="1kB",
            tgts_per_mshr=12,
            addr_ranges=board.mem_ranges,
        )
        self.iocache.mem_side = self.membus.cpu_side_ports
        self.iocache.cpu_side = board.get_mem_side_coherent_io_port()
