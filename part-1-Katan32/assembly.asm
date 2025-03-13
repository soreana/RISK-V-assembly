    .section .data
    .global result_L1
    .global result_L2

result_L1:  .word 0
result_L2:  .word 0

    .section .text
    .global my_assembly_function

my_assembly_function:
    # -----------------------------------------
    # Initialize constants and masks
    # -----------------------------------------
    li t0, 0x12345678     # Full 32-bit state
    li a1, 0x1FFF         # Mask for 13 bits (L1)
    li a2, 0x7FFFF        # Mask for 19 bits (L2)
    li t4, 1              # IR = 1
    li t5, 0              # ka = 0
    li t6, 1              # kb = 1

    # -----------------------------------------
    # Correct split into L1 (upper 13 bits), L2 (lower 19 bits)
    # -----------------------------------------
    srli t1, t0, 19       # L1 = state >> 19
    and  t1, t1, a1       # Mask upper 13 bits

    and  t2, t0, a2       # L2 = state & 0x7FFFF (lower 19 bits)


    # -----------------------------------------
    # ---- Compute fa ----
    # fa = L1[12] ^ L1[7] ^ (L1[8] & L1[5]) ^ (L1[3] & IR) ^ ka
    # -----------------------------------------

    srl s0, t1, 12        # L1[12]
    and s0, s0, 1

    srl s1, t1, 7         # L1[7]
    and s1, s1, 1

    srl s2, t1, 8         # L1[8]
    and s2, s2, 1

    srl s3, t1, 5         # L1[5]
    and s3, s3, 1

    and s4, s2, s3        # (L1[8] & L1[5])

    srl s5, t1, 3         # L1[3]
    and s5, s5, 1

    and s5, s5, t4        # (L1[3] & IR)

    xor s10, s0, s1
    xor s10, s10, s4
    xor s10, s10, s5
    xor s10, s10, t5      # XOR ka (0), structurally kept
    and s10, s10, 1       # fa (final value in s6)

    # -----------------------------------------
    # ---- Compute fb = L2[18] ^ L2[7] ^ (L2[12] & L2[10]) ^ (L2[8] & L2[3]) ^ kb
    # -----------------------------------------

    srl s0, t2, 18        # L2[18]
    and s0, s0, 1

    srl s1, t2, 7         # L2[7]
    and s1, s1, 1

    srl s2, t2, 12        # L2[12]
    and s2, s2, 1

    srl s3, t2, 10        # L2[10]
    and s3, s3, 1

    srl s4, t2, 8         # L2[8]
    and s4, s4, 1

    srl s5, t2, 3         # L2[3]
    and s5, s5, 1

    and s3, s3, s2        # L2[12] & L2[10]
    and s5, s5, s4        # L2[8] & L2[3]

    xor s11, s0, s1
    xor s11, s11, s3
    xor s11, s11, s5
    xor s11, s11, t6       # XOR kb
    and s11, s11, 1        # fb (final value in s4)

    # -----------------------------------------
    # ---- Shift and insert fa and fb ----
    # -----------------------------------------

    slli t1, t1, 1        # Shift L1 left by 1
    or t1, t1, s11         # Insert fb
    and t1, t1, a1        # Mask to 13 bits

    slli t2, t2, 1        # Shift L2 left by 1
    or t2, t2, s10        # Insert fa
    and t2, t2, a2        # Mask to 19 bits

    # -----------------------------------------
    # ---- Store results ----
    # -----------------------------------------

    la s0, result_L1      # Address of result_L1
    sw t1, 0(s0)          # Store L1

    la s1, result_L2      # Address of result_L2
    sw t2, 0(s1)          # Store L2

    ret                  # Return from function
