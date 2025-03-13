# KATAN32 One-Round Implementation in RISC-V Assembly

## Overview

This project contains a **RISC-V assembly implementation of a single round of the KATAN32 block cipher**, following the official specification and using correct bit splitting between L1 and L2. The implementation is designed to run on a RISC-V environment using **SEGGER Embedded Studio (SES)**.

---

## Project Structure

| File           | Description                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| `main.c`       | C code to call the assembly function and print results.                                                    |
| `assembly.asm` | RISC-V assembly implementing KATAN32 1 round computation.                                                  |
| `reference/`   | Directory containing reference Python implementations used for understanding and cross-verification.       |

---

## Key Highlights

- **One round of KATAN32** executed directly in assembly.
- **Proper bit splitting**:
  - **L1**: upper 13 bits of the 32-bit state.
  - **L2**: lower 19 bits of the 32-bit state.
- Fully aligned with **official KATAN32 tap positions**.
- Configured for test input `0x12345678`.
- Computes and stores updated `L1` and `L2` after one round.

---

## How It Works

1. **State Initialization**:\
   The 32-bit state `0x12345678` is split as:

   - `L1 = state[31:19]` (upper 13 bits)
   - `L2 = state[18:0]` (lower 19 bits)

2. **fa computation (Feedback for L1)**:

```
fa = L1[12] ⊕ L1[7] ⊕ (L1[8] & L1[5]) ⊕ (L1[3] & IR) ⊕ ka
```

3. **fb computation (Feedback for L2)**:

```
fb = L2[18] ⊕ L2[7] ⊕ (L2[12] & L2[10]) ⊕ (L2[8] & L2[3]) ⊕ kb
```

4. **Shift and update L1 and L2**:

   - L1 is shifted left and fb is inserted as a feedback bit.
   - L2 is shifted left and fa is inserted as a feedback bit.
   - Final L1 and L2 are masked to their respective lengths (13 and 19 bits).

5. **Results**:

   - Stored in `result_L1` and `result_L2`, accessible from C for verification or further processing.

---

## ✅ Example Output (Expected after 1 round)

```plaintext
L1 after 1 round: 0xXXXX  # Final 13-bit L1
L2 after 1 round: 0xYYYYY # Final 19-bit L2
```

---

## 📚 References

1. **Reference Implementation**:

   - Python code for KATAN32 available at:\
     [https://github.com/saikumargadde2807/Python-Codes-for-KATAN-and-AES-security-algorithms](https://github.com/saikumargadde2807/Python-Codes-for-KATAN-and-AES-security-algorithms)
   - Used for understanding algorithm flow and verifying bit operations.

2. **Cryptanalysis Reference**:

   - *Cryptanalysis of Reduced-Round KATAN and KTANTAN Block Ciphers*\
     [https://eprint.iacr.org/2018/258.pdf](https://eprint.iacr.org/2018/258.pdf)
---

## Running the Code

### Requirements:

- SEGGER Embedded Studio

### Build and Run:

1. Open the project in SEGGER Embedded Studio.
2. Add `main.c` and `assembly.asm` to your project.
3. Build and run the project on RISC-V target.
4. Observe the output in console (J-Link RTT, UART, or terminal depending on setup).

---

## Notes

- The reference implementations in the `reference/` directory have been **adjusted to support one-round testing**, to match this assembly output for validation.
- This project focuses **on one round only**
