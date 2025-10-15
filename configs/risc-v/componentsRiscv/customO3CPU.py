from componentsRiscv.customBranchPredictor import (
    PerceptBP,
    TournBP,
    TAGE_BP
)
from componentsRiscv.customFUPool import FUP_Big, FUP_Small, FUP_General

from m5.objects import (
    RiscvO3CPU,
    DefaultFUPool,
    TournamentBP
)

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA


# O3Core extiende X86O3CPU. X86O3CPU es uno de los modelos internos de gem5 que implementa
# un pipeline fuera de orden para la arquitectura x86.
class RiscvO3Core(RiscvO3CPU):
    def __init__(
        self,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        fu_pool,
        bp,
        numEntriesBtb=None,
        numEntriesRas=None,
        tagBitsBtb=None,
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        num_ports=None,  # Optional parameter for "General" fu_pool
        num_IQs=None,
        num_DividedIQ_entries=None,
        fetchWidth=None,
        decodeWidth=None,
        renameWidth=None,
        issueWidth=None,
        dispatchWidth=None,
        commitWidth=None,
        wbWidth=None,
        lsq_size=None,
        lq_entries=None,
        sq_entries=None,
    ):
        super().__init__()

        # Set pipeline widths, defaulting to frontend_width or backend_width if not specified
        self.fetchWidth = fetchWidth if fetchWidth is not None else frontend_width
        self.decodeWidth = decodeWidth if decodeWidth is not None else frontend_width
        self.renameWidth = renameWidth if renameWidth is not None else frontend_width
        self.issueWidth = issueWidth if issueWidth is not None else backend_width
        self.dispatchWidth = dispatchWidth if dispatchWidth is not None else backend_width
        self.commitWidth = commitWidth if commitWidth is not None else backend_width
        self.wbWidth = wbWidth if wbWidth is not None else backend_width

        # Set sizes of ROB, IQ, LQ, SQ and reg files
        self.numROBEntries = rob_size
        self.numIQEntries = iq_size
        # Ensure LSQ sizing is valid: either a common lsq_size is provided
        # or both lq_entries and sq_entries are specified separately.
        if lsq_size is None and (lq_entries is None or sq_entries is None):
            raise ValueError(
                "Either 'lsq_size' must be provided or both 'lq_entries' and 'sq_entries' must be provided"
            )
        self.LQEntries = lq_entries if lq_entries is not None else lsq_size
        self.SQEntries = sq_entries if sq_entries is not None else lsq_size

        self.numPhysIntRegs = num_int_phys_regs
        self.numPhysFloatRegs = num_fp_phys_regs

        # Configure Functional Unit Pool
        valid_fu_pools = ["Big", "Small", "XT-910", "General", "Default"]
        if fu_pool not in valid_fu_pools:
            raise ValueError(f"Invalid fu_pool '{fu_pool}'. Valid options are: {valid_fu_pools}")

        if fu_pool == "Big":
            self.fuPool = FUP_Big()
        elif fu_pool == "Small":
            self.fuPool = FUP_Small()
        elif fu_pool == "General":
            if num_ports is None:
                raise ValueError("num_ports must be specified for 'General' fu_pool")
            self.fuPool = FUP_General(num_ports)
        elif fu_pool == "XT-910":
            self.fuPool = FUP_XT910()
        else:
            self.fuPool = DefaultFUPool()

        # Configure Branch Predictor
        valid_bps = ["TournBP", "PerceptBP", "TAGE_BP", "Default"]
        if bp not in valid_bps:
            raise ValueError(f"Invalid bp '{bp}'. Valid options are: {valid_bps}")

        if bp == "TournBP":
            if numEntriesBtb is None or numEntriesRas is None:
                raise ValueError("numEntriesBtb and numEntriesRas must be provided for 'TournBP'")
            self.branchPred = TournBP(
                numEntriesBtb, 
                numEntriesRas, 
            )
        elif bp == "TAGE_BP":
            self.branchPred = TAGE_BP() # TODO: parametrizar
        elif bp == "PerceptBP":
            if numEntriesBtb is None or numEntriesRas is None:
                raise ValueError("numEntriesBtb and numEntriesRas must be provided for 'PerceptBP'")
            self.branchPred = PerceptBP(
                numEntriesBtb,
                tagBitsBtb,
                numEntriesRas,
                num_filter_entries,
                num_local_histories,
                local_history_length,
            )
        else:
            self.branchPred = TournamentBP()

        # Configure Distributed IQ
        if num_IQs and num_DividedIQ_entries:
            self.numIQs = num_IQs
            self.numEntriesDividedIQ = num_DividedIQ_entries


# O3StdCore hace wrap de O3CPUCore a un core compatible con la libreria estandar de gem5.
class RiscvO3StdCore(BaseCPUCore):
    def __init__(
        self,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        fu_pool,
        bp,
        numEntriesBtb=None,
        numEntriesRas=None,
        tagBitsBtb=None,        
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        num_ports=None,
        num_IQs=None,
        num_DividedIQ_entries=None,
        fetchWidth=None,
        decodeWidth=None,
        renameWidth=None,
        issueWidth=None,
        dispatchWidth=None,
        commitWidth=None,
        wbWidth=None,
        lsq_size=None,
        lq_entries=None,
        sq_entries=None,
    ):
        core = RiscvO3Core(
            frontend_width,
            backend_width,
            rob_size,
            iq_size,
            num_int_phys_regs,
            num_fp_phys_regs,
            fu_pool,
            bp,
            numEntriesBtb,
            numEntriesRas,
            tagBitsBtb,
            num_filter_entries,
            num_local_histories,
            local_history_length,
            num_ports,
            num_IQs,
            num_DividedIQ_entries,
            fetchWidth,
            decodeWidth,
            renameWidth,
            issueWidth,
            dispatchWidth,
            commitWidth,
            wbWidth,
            lsq_size,
            lq_entries,
            sq_entries,
        )
        super().__init__(core, ISA.RISCV)


# O3Processor, junto con BaseCPUProcessor, hace wrap de O3Core a un procesador compatible con la libreria estandar de gem5.
class RiscvO3Processor(BaseCPUProcessor):
    def __init__(
        self,
        numCores,
        frontend_width,
        backend_width,
        rob_size,
        iq_size,
        num_int_phys_regs,
        num_fp_phys_regs,
        fu_pool,
        bp,
        numEntriesBtb=None,
        numEntriesRas=None,
        tagBitsBtb=None,        
        num_filter_entries=None,
        num_local_histories=None,
        local_history_length=None,
        num_ports=None,
        num_IQs=None,
        num_DividedIQ_entries=None,
        fetchWidth=None,
        decodeWidth=None,
        renameWidth=None,
        issueWidth=None,
        dispatchWidth=None,
        commitWidth=None,
        wbWidth=None,
        lsq_size=None,
        lq_entries=None,
        sq_entries=None,
    ):
        cores = [
            RiscvO3StdCore(
                frontend_width,
                backend_width,
                rob_size,
                iq_size,
                num_int_phys_regs,
                num_fp_phys_regs,
                fu_pool,
                bp,
                numEntriesBtb,
                numEntriesRas,
                tagBitsBtb,
                num_filter_entries,
                num_local_histories,
                local_history_length,
                num_ports,
                num_IQs,
                num_DividedIQ_entries,
                fetchWidth,
                decodeWidth,
                renameWidth,
                issueWidth,
                dispatchWidth,
                commitWidth,
                wbWidth,
                lsq_size,
                lq_entries,
                sq_entries,
            )
            for _ in range(numCores)
        ]
        super().__init__(cores)
