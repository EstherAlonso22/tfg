from m5.objects import (
    FUDesc,
    FUPool,
    OpDesc,
)

# FUDesc como puerto funcional, OpDesc son las diferentes "unidades funcionales" que tiene el puerto

# Configuracion bigO3
# Puertos:
class P0_Big(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="FloatMisc"),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=2),
        OpDesc(opClass="SimdFloatAlu", opLat=2),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=2),
        OpDesc(opClass="SimdFloatCvt", opLat=2),
        OpDesc(opClass="SimdMult", opLat=2),
        OpDesc(opClass="SimdFloatMult", opLat=2),
        OpDesc(opClass="SimdMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMultAcc", opLat=2),
        OpDesc(opClass="SimdDiv", opLat=2),
        OpDesc(opClass="SimdFloatDiv", opLat=2),
        OpDesc(opClass="SimdMisc", opLat=2),
        OpDesc(opClass="SimdFloatMisc", opLat=2),
        OpDesc(opClass="SimdSqrt", opLat=3),
        OpDesc(opClass="SimdFloatSqrt", opLat=3),
        OpDesc(opClass="SimdShift", opLat=2),
        OpDesc(opClass="SimdShiftAcc", opLat=2),
    ]
    count = 1

class P1_Big(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="IntDiv", opLat=2),
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=2),
        OpDesc(opClass="SimdFloatAlu", opLat=2),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=2),
        OpDesc(opClass="SimdFloatCvt", opLat=2),
        OpDesc(opClass="SimdMult", opLat=2),
        OpDesc(opClass="SimdFloatMult", opLat=2),
        OpDesc(opClass="SimdMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMultAcc", opLat=2),
        OpDesc(opClass="SimdShift", opLat=2),
        OpDesc(opClass="SimdShiftAcc", opLat=2),
    ]
    count = 1

class P2_Big(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskLoad", opLat=2),
        OpDesc(opClass="SimdStridedLoad", opLat=2),
        OpDesc(opClass="SimdIndexedLoad", opLat=2),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad", opLat=2),
    ]
    count = 1

class P3_Big(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskLoad", opLat=2),
        OpDesc(opClass="SimdStridedLoad", opLat=2),
        OpDesc(opClass="SimdIndexedLoad", opLat=2),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad", opLat=2),
    ]
    count = 1

class P4_Big(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="SimdUnitStrideStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskStore", opLat=2),
        OpDesc(opClass="SimdStridedStore", opLat=2),
        OpDesc(opClass="SimdIndexedStore", opLat=2),
        OpDesc(opClass="SimdWholeRegisterStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedStore", opLat=2),
    ]
    count = 1

class P5_Big(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        OpDesc(opClass="SimdMatMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMatMultAcc", opLat=2),
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=2),
        OpDesc(opClass="SimdFloatAlu", opLat=2),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=2),
        OpDesc(opClass="SimdFloatCvt", opLat=2),
        OpDesc(opClass="SimdMult", opLat=2),
        OpDesc(opClass="SimdFloatMult", opLat=2),
        OpDesc(opClass="SimdMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMultAcc", opLat=2),
    ]
    count = 1

class P6_Big(FUDesc):
    opList = [OpDesc(opClass="IntAlu")]
    count = 1

# Puertos STA
# class P7_Big(FUDesc):
#     opList = []
#     count = 1


# class P8_Big(FUDesc):
#     opList = []
#     count = 1

class P9_Big(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="SimdUnitStrideStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskStore", opLat=2),
        OpDesc(opClass="SimdStridedStore", opLat=2),
        OpDesc(opClass="SimdIndexedStore", opLat=2),
        OpDesc(opClass="SimdWholeRegisterStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedStore", opLat=2),
    ]
    count = 1

class P10_Big(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskLoad", opLat=2),
        OpDesc(opClass="SimdStridedLoad", opLat=2),
        OpDesc(opClass="SimdIndexedLoad", opLat=2),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad", opLat=2),
    ]
    count = 1

class P11_Big(FUDesc):
    opList = [OpDesc(opClass="IntAlu")]
    count = 1

# Puerto extra con las cosas raras, en principio debería usarse poco
class PX_Big(FUDesc):
    opList = [
        OpDesc(opClass="IprAccess"),
        OpDesc(opClass="InstPrefetch"),
        OpDesc(opClass="SimdExt", opLat=2),
        OpDesc(opClass="SimdFloatExt", opLat=2),
        OpDesc(opClass="SimdConfig"),
        OpDesc(opClass="SimdReduceAdd", opLat=2),
        OpDesc(opClass="SimdReduceAlu", opLat=2),
        OpDesc(opClass="SimdReduceCmp", opLat=2),
        OpDesc(opClass="SimdFloatReduceAdd", opLat=2),
        OpDesc(opClass="SimdFloatReduceCmp", opLat=2),
        OpDesc(opClass="SimdAes", opLat=2),
        OpDesc(opClass="SimdAesMix", opLat=2),
        OpDesc(opClass="SimdSha1Hash", opLat=2),
        OpDesc(opClass="SimdSha1Hash2", opLat=2),
        OpDesc(opClass="SimdSha256Hash", opLat=2),
        OpDesc(opClass="SimdSha256Hash2", opLat=2),
        OpDesc(opClass="SimdShaSigma2", opLat=2),
        OpDesc(opClass="SimdShaSigma3", opLat=2),
        OpDesc(opClass="SimdPredAlu", opLat=2),
    ]
    count = 1

# Pool con todos los puertos
class FUP_Big(FUPool):
    FUList = [P0_Big(), P1_Big(), P2_Big(),  P3_Big(), P4_Big(), P5_Big(), P6_Big(), P9_Big(), P10_Big(), P11_Big(), PX_Big()]

# -----------------------------------------------------------------------------------------------
# Configuracion smallO3
# Puertos:
class P0_Small(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu")
    ]
    count = 1

class P1_Small(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu")
    ]
    count = 1

class P2_Small(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="IntDiv", opLat=2),
    ]
    count = 1

class P3_Small(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ]
    count = 1

class P4_Small(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
    ]
    count = 1

class P5_Small(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="SimdAdd", opLat=4),
        OpDesc(opClass="SimdAddAcc", opLat=4),
        OpDesc(opClass="SimdAlu", opLat=4),
        OpDesc(opClass="SimdCmp", opLat=4),
        OpDesc(opClass="SimdCvt", opLat=4),
        OpDesc(opClass="SimdMult", opLat=4),
        OpDesc(opClass="SimdMultAcc", opLat=4),
        OpDesc(opClass="SimdShift", opLat=4),
        OpDesc(opClass="SimdShiftAcc", opLat=4),
        OpDesc(opClass="SimdFloatAdd", opLat=4),
        OpDesc(opClass="SimdFloatAlu", opLat=4),
        OpDesc(opClass="SimdFloatCmp", opLat=4),
        OpDesc(opClass="SimdFloatCvt", opLat=4),
        OpDesc(opClass="SimdFloatMult", opLat=4),
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
    ]
    count = 1

class P6_Small(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="FloatMisc"),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=4),
        OpDesc(opClass="SimdAddAcc", opLat=4),
        OpDesc(opClass="SimdAlu", opLat=4),
        OpDesc(opClass="SimdCmp", opLat=4),
        OpDesc(opClass="SimdCvt", opLat=4),
        OpDesc(opClass="SimdMult", opLat=4),
        OpDesc(opClass="SimdMultAcc", opLat=4),
        OpDesc(opClass="SimdShift", opLat=4),
        OpDesc(opClass="SimdShiftAcc", opLat=4),
        OpDesc(opClass="SimdFloatAdd", opLat=4),
        OpDesc(opClass="SimdFloatAlu", opLat=4),
        OpDesc(opClass="SimdFloatCmp", opLat=4),
        OpDesc(opClass="SimdFloatCvt", opLat=4),
        OpDesc(opClass="SimdFloatMult", opLat=4),
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
        OpDesc(opClass="SimdDiv", opLat=4),
        OpDesc(opClass="SimdFloatDiv", opLat=4),
        OpDesc(opClass="SimdSqrt", opLat=4),
        OpDesc(opClass="SimdFloatSqrt", opLat=4),
    ]
    count = 1

class PX_Small(FUDesc):
    opList = [
        OpDesc(opClass="SimdMisc"),
        OpDesc(opClass="SimdFloatMisc"),
        OpDesc(opClass="SimdFloatMatMultAcc"),
        OpDesc(opClass="SimdReduceAdd"),
        OpDesc(opClass="SimdReduceAlu"),
        OpDesc(opClass="SimdReduceCmp"),
        OpDesc(opClass="SimdFloatReduceAdd"),
        OpDesc(opClass="SimdFloatReduceCmp"),
        OpDesc(opClass="SimdAes"),
        OpDesc(opClass="SimdAesMix"),
        OpDesc(opClass="SimdSha1Hash"),
        OpDesc(opClass="SimdSha1Hash2"),
        OpDesc(opClass="SimdSha256Hash"),
        OpDesc(opClass="SimdSha256Hash2"),
        OpDesc(opClass="SimdShaSigma2"),
        OpDesc(opClass="SimdShaSigma3"),
        OpDesc(opClass="SimdPredAlu"),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        OpDesc(opClass="IprAccess"),
        OpDesc(opClass="InstPrefetch"),
        OpDesc(opClass="SimdUnitStrideLoad"),
        OpDesc(opClass="SimdUnitStrideStore"),
        OpDesc(opClass="SimdUnitStrideMaskLoad"),
        OpDesc(opClass="SimdUnitStrideMaskStore"),
        OpDesc(opClass="SimdStridedLoad"),
        OpDesc(opClass="SimdStridedStore"),
        OpDesc(opClass="SimdIndexedLoad"),
        OpDesc(opClass="SimdIndexedStore"),
        OpDesc(opClass="SimdWholeRegisterLoad"),
        OpDesc(opClass="SimdWholeRegisterStore"),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedStore"),
        OpDesc(opClass="SimdExt"),
        OpDesc(opClass="SimdFloatExt"),
        OpDesc(opClass="SimdConfig"),
    ]
    count = 1

# Pool con todos los puertos
class FUP_Small(FUPool):
   FUList = [P0_Small(), P1_Small(), P2_Small(),  P3_Small(), P4_Small(), P5_Small(), P6_Small(), PX_Small()]


# ------------------------------------------------------------------------------------------------------------
# Configuracion generalizada
# Puerto general con todas las unidades funcionales:
class PGeneral(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu"),
        OpDesc(opClass="IntMult"),
        OpDesc(opClass="IntDiv", opLat=2),
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult"),
        OpDesc(opClass="FloatMultAcc"),
        OpDesc(opClass="FloatDiv", opLat=2),
        OpDesc(opClass="FloatMisc"),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=2),
        OpDesc(opClass="SimdAddAcc", opLat=2),
        OpDesc(opClass="SimdAlu", opLat=2),
        OpDesc(opClass="SimdCmp", opLat=2),
        OpDesc(opClass="SimdCvt", opLat=2),
        OpDesc(opClass="SimdMisc", opLat=2),
        OpDesc(opClass="SimdMult", opLat=2),
        OpDesc(opClass="SimdMultAcc", opLat=2),
        OpDesc(opClass="SimdMatMultAcc", opLat=2),
        OpDesc(opClass="SimdShift", opLat=2),
        OpDesc(opClass="SimdShiftAcc", opLat=2),
        OpDesc(opClass="SimdDiv", opLat=2),
        OpDesc(opClass="SimdSqrt", opLat=3),
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        OpDesc(opClass="SimdFloatAlu", opLat=2),
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        OpDesc(opClass="SimdFloatCvt", opLat=2),
        OpDesc(opClass="SimdFloatDiv", opLat=2),
        OpDesc(opClass="SimdFloatMisc", opLat=2),
        OpDesc(opClass="SimdFloatMult", opLat=2),
        OpDesc(opClass="SimdFloatMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatMatMultAcc", opLat=2),
        OpDesc(opClass="SimdFloatSqrt", opLat=3),
        OpDesc(opClass="SimdReduceAdd", opLat=2),
        OpDesc(opClass="SimdReduceAlu", opLat=2),
        OpDesc(opClass="SimdReduceCmp", opLat=2),
        OpDesc(opClass="SimdFloatReduceAdd", opLat=2),
        OpDesc(opClass="SimdFloatReduceCmp", opLat=2),
        OpDesc(opClass="SimdAes", opLat=2),
        OpDesc(opClass="SimdAesMix", opLat=2),
        OpDesc(opClass="SimdSha1Hash", opLat=2),
        OpDesc(opClass="SimdSha1Hash2", opLat=2),
        OpDesc(opClass="SimdSha256Hash", opLat=2),
        OpDesc(opClass="SimdSha256Hash2", opLat=2),
        OpDesc(opClass="SimdShaSigma2", opLat=2),
        OpDesc(opClass="SimdShaSigma3", opLat=2),
        OpDesc(opClass="SimdPredAlu", opLat=2),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="FloatMemWrite"),
        OpDesc(opClass="IprAccess"),
        OpDesc(opClass="InstPrefetch"),
        OpDesc(opClass="SimdUnitStrideLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideMaskStore", opLat=2),
        OpDesc(opClass="SimdStridedLoad", opLat=2),
        OpDesc(opClass="SimdStridedStore", opLat=2),
        OpDesc(opClass="SimdIndexedLoad", opLat=2),
        OpDesc(opClass="SimdIndexedStore", opLat=2),
        OpDesc(opClass="SimdWholeRegisterLoad", opLat=2),
        OpDesc(opClass="SimdWholeRegisterStore", opLat=2),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad", opLat=2),
        OpDesc(opClass="SimdUnitStrideSegmentedStore", opLat=2),
        OpDesc(opClass="SimdExt", opLat=2),
        OpDesc(opClass="SimdFloatExt", opLat=2),
        OpDesc(opClass="SimdConfig"),
    ]
    count = 1

class FUP_General(FUPool):
    def __init__(self, num_ports):
        super().__init__()
        self.FUList = [PGeneral() for _ in range(num_ports)]

# ------------------------------------------------------------------------------------------------------------
# Configuracion XT-910

# Puertos 0 y 1: las 3 pipes de load/store 
class P0_XT910(FUDesc):
    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
    ]
    count = 1

class P1_XT910(FUDesc):
    opList = [
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
    ]
    # TODO: Review 
    count = 2 # The pseudo double store instruction

# class P2_XT910(FUDesc): 1 pipe de branch, no branch unit en gem5

# Puertos 3 y 4: las 2 pipes de arithmetic operation instructions
class P3_XT910(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu", opLat=2),
        OpDesc(opClass="IprAccess", opLat=3, pipelined=True), # Como ex5
        OpDesc(opClass="IntDiv", opLat=6),
    ]
    count = 1

class P4_XT910(FUDesc):
    opList = [
        OpDesc(opClass="IntAlu", opLat=1),
        OpDesc(opClass="IntMult", opLat=1), 
    ]
    count = 1

class P5_XT910(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult", opLat=5),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatDiv", opLat=6),
        OpDesc(opClass="FloatMisc"),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=3),
        OpDesc(opClass="SimdAddAcc", opLat=3),
        OpDesc(opClass="SimdAlu", opLat=3),
        OpDesc(opClass="SimdCmp", opLat=3),
        OpDesc(opClass="SimdCvt", opLat=3),
        OpDesc(opClass="SimdMult", opLat=5),
        OpDesc(opClass="SimdMultAcc", opLat=5),
        OpDesc(opClass="SimdShift", opLat=3),
        OpDesc(opClass="SimdShiftAcc", opLat=3),
        OpDesc(opClass="SimdFloatAdd", opLat=3),
        OpDesc(opClass="SimdFloatAlu", opLat=3),
        OpDesc(opClass="SimdFloatCmp", opLat=3),
        OpDesc(opClass="SimdFloatCvt", opLat=3),
        OpDesc(opClass="SimdFloatMult", opLat=5),
        OpDesc(opClass="SimdFloatMultAcc", opLat=5),
        OpDesc(opClass="SimdDiv", opLat=6),
        OpDesc(opClass="SimdFloatDiv", opLat=6),
        OpDesc(opClass="SimdSqrt", opLat=3),
        OpDesc(opClass="SimdFloatSqrt", opLat=3),
    ]
    count = 1 #TODO: revisar, cada uno de estos tiene 4 FUs internas, seria 4?

class P6_XT910(FUDesc):
    opList = [
        OpDesc(opClass="FloatAdd"),
        OpDesc(opClass="FloatCmp"),
        OpDesc(opClass="FloatCvt"),
        OpDesc(opClass="FloatMult", opLat=5),
        OpDesc(opClass="FloatMultAcc", opLat=5),
        OpDesc(opClass="FloatDiv", opLat=6),
        OpDesc(opClass="FloatMisc"),
        OpDesc(opClass="FloatSqrt", opLat=3),
        OpDesc(opClass="SimdAdd", opLat=3),
        OpDesc(opClass="SimdAddAcc", opLat=3),
        OpDesc(opClass="SimdAlu", opLat=3),
        OpDesc(opClass="SimdCmp", opLat=3),
        OpDesc(opClass="SimdCvt", opLat=3),
        OpDesc(opClass="SimdMult", opLat=5),
        OpDesc(opClass="SimdMultAcc", opLat=5),
        OpDesc(opClass="SimdShift", opLat=3),
        OpDesc(opClass="SimdShiftAcc", opLat=3),
        OpDesc(opClass="SimdFloatAdd", opLat=3),
        OpDesc(opClass="SimdFloatAlu", opLat=3),
        OpDesc(opClass="SimdFloatCmp", opLat=3),
        OpDesc(opClass="SimdFloatCvt", opLat=3),
        OpDesc(opClass="SimdFloatMult", opLat=5),
        OpDesc(opClass="SimdFloatMultAcc", opLat=5),
        OpDesc(opClass="SimdDiv", opLat=6),
        OpDesc(opClass="SimdFloatDiv", opLat=6),
        OpDesc(opClass="SimdSqrt", opLat=3),
        OpDesc(opClass="SimdFloatSqrt", opLat=3),
    ]
    count = 1 #TODO

class PX_XT910(FUDesc):
    opList = [
        OpDesc(opClass="SimdMisc"),
        OpDesc(opClass="SimdFloatMisc"),
        OpDesc(opClass="SimdFloatMatMultAcc"),
        OpDesc(opClass="SimdReduceAdd"),
        OpDesc(opClass="SimdReduceAlu"),
        OpDesc(opClass="SimdReduceCmp"),
        OpDesc(opClass="SimdFloatReduceAdd"),
        OpDesc(opClass="SimdFloatReduceCmp"),
        OpDesc(opClass="SimdAes"),
        OpDesc(opClass="SimdAesMix"),
        OpDesc(opClass="SimdSha1Hash"),
        OpDesc(opClass="SimdSha1Hash2"),
        OpDesc(opClass="SimdSha256Hash"),
        OpDesc(opClass="SimdSha256Hash2"),
        OpDesc(opClass="SimdShaSigma2"),
        OpDesc(opClass="SimdShaSigma3"),
        OpDesc(opClass="SimdPredAlu"),
        OpDesc(opClass="Matrix"),
        OpDesc(opClass="MatrixMov"),
        OpDesc(opClass="MatrixOP"),
        OpDesc(opClass="IprAccess"),
        OpDesc(opClass="InstPrefetch"),
        OpDesc(opClass="SimdUnitStrideLoad"),
        OpDesc(opClass="SimdUnitStrideStore"),
        OpDesc(opClass="SimdUnitStrideMaskLoad"),
        OpDesc(opClass="SimdUnitStrideMaskStore"),
        OpDesc(opClass="SimdStridedLoad"),
        OpDesc(opClass="SimdStridedStore"),
        OpDesc(opClass="SimdIndexedLoad"),
        OpDesc(opClass="SimdIndexedStore"),
        OpDesc(opClass="SimdWholeRegisterLoad"),
        OpDesc(opClass="SimdWholeRegisterStore"),
        OpDesc(opClass="SimdUnitStrideFaultOnlyFirstLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedLoad"),
        OpDesc(opClass="SimdUnitStrideSegmentedStore"),
        OpDesc(opClass="SimdExt"),
        OpDesc(opClass="SimdFloatExt"),
        OpDesc(opClass="SimdConfig"),
    ]
    count = 1

class FUP_XT910(FUPool):
    FUList = [P0_XT910(), P1_XT910(), P3_XT910(), P4_XT910(), P5_XT910(), P6_XT910(), PX_XT910()]