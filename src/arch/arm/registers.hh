#ifndef __ARCH_ARM_REGISTERS_HH__
#define __ARCH_ARM_REGISTERS_HH__

#include "arch/arm/ccregs.hh"
#include "arch/arm/generated/max_inst_regs.hh"
#include "arch/arm/intregs.hh"
#include "arch/arm/miscregs.hh"
#include "arch/arm/types.hh"
#include "arch/generic/vec_pred_reg.hh"
#include "arch/generic/vec_reg.hh"

namespace ArmISA {


// For a predicated instruction, we need all the
// destination registers to also be sources
const int MaxInstSrcRegs = ArmISAInst::MaxInstDestRegs +
    ArmISAInst::MaxInstSrcRegs;
using ArmISAInst::MaxInstDestRegs;
using ArmISAInst::MaxMiscDestRegs;

// Number of VecElem per Vector Register considering only pre-SVE
// Advanced SIMD registers.
constexpr unsigned NumVecElemPerNeonVecReg = 4;
// Number of VecElem per Vector Register, computed based on the vector length
constexpr unsigned NumVecElemPerVecReg = MaxSveVecLenInWords;

using VecElem = uint32_t;
using VecReg = ::VecRegT<VecElem, NumVecElemPerVecReg, false>;
using ConstVecReg = ::VecRegT<VecElem, NumVecElemPerVecReg, true>;
using VecRegContainer = VecReg::Container;

using VecPredReg = ::VecPredRegT<VecElem, NumVecElemPerVecReg,
                                 VecPredRegHasPackedRepr, false>;
using ConstVecPredReg = ::VecPredRegT<VecElem, NumVecElemPerVecReg,
                                      VecPredRegHasPackedRepr, true>;
using VecPredRegContainer = VecPredReg::Container;

// Constants Related to the number of registers
// Int, Float, CC, Misc
const int NumIntArchRegs = NUM_ARCH_INTREGS;
const int NumIntRegs = NUM_INTREGS;
const int NumFloatRegs = 0; // Float values are stored in the VecRegs
const int NumCCRegs = NUM_CCREGS;
const int NumMiscRegs = NUM_MISCREGS;

// Vec, PredVec
// NumFloatV7ArchRegs: This in theory should be 32.
// However in A32 gem5 is splitting double register accesses in two
// subsequent single register ones. This means we would use a index
// bigger than 31 when accessing D16-D31.
const int NumFloatV7ArchRegs = 64; // S0-S31, D0-D31
const int NumVecV7ArchRegs  = 16; // Q0-Q15
const int NumVecV8ArchRegs  = 32; // V0-V31
const int NumVecSpecialRegs = 8;
const int NumVecIntrlvRegs = 4;
const int NumVecRegs = NumVecV8ArchRegs + NumVecSpecialRegs + NumVecIntrlvRegs;
const int NumVecPredRegs = 18;  // P0-P15, FFR, UREG0

const int TotalNumRegs = NumIntRegs + NumFloatRegs + NumVecRegs +
    NumVecPredRegs + NumMiscRegs;

// Semantically meaningful register indices
const int ReturnValueReg = 0;
const int ReturnValueReg1 = 1;
const int ReturnValueReg2 = 2;
const int NumArgumentRegs = 4;
const int NumArgumentRegs64 = 8;
const int ArgumentReg0 = 0;
const int ArgumentReg1 = 1;
const int ArgumentReg2 = 2;
const int ArgumentReg3 = 3;
const int FramePointerReg = 11;
const int StackPointerReg = INTREG_SP;
const int ReturnAddressReg = INTREG_LR;
const int PCReg = INTREG_PC;

const int ZeroReg = INTREG_ZERO;

// Vec, PredVec indices
const int VecSpecialElem = NumVecV8ArchRegs * NumVecElemPerNeonVecReg;
const int INTRLVREG0 = NumVecV8ArchRegs + NumVecSpecialRegs;
const int INTRLVREG1 = INTRLVREG0 + 1;
const int INTRLVREG2 = INTRLVREG0 + 2;
const int INTRLVREG3 = INTRLVREG0 + 3;
const int VECREG_UREG0 = 32;
const int PREDREG_FFR = 16;
const int PREDREG_UREG0 = 17;

const int SyscallNumReg = ReturnValueReg;
const int SyscallPseudoReturnReg = ReturnValueReg;
const int SyscallSuccessReg = ReturnValueReg;

} // namespace ArmISA

#endif
