.section .data
.global result_L1
.global result_L2

result_L1:  .word 0
result_L2:  .word 0

block_L1:   .word 0x44556677    # Lower 32 bits of block (0x0011223344556677)
block_L2:   .word 0x00112233    # Upper 32 bits of block

key_L1:     .word 0xccddeeff    # Lower 32 bits of key (0x8899aabbccddeeff)
key_L2:     .word 0x8899aabb    # Upper 32 bits of key

.section .text
.global my_assembly_function

my_assembly_function:
    // Load block
    la t0, block_L1
    lw t1, 0(t0)
    lw t2, 4(t0)

    // Load key
    la t3, key_L1
    lw t4, 0(t3)
    lw t5, 4(t3)

    // AddRoundKey (XOR block with key)
    xor s1, t1, t4
    xor s2, t2, t5


    // |  Col 15  |  Col 14  | ... |  Col 0  |
    // |----------|----------|-----|---------|
    // |  a0,15   |  a0,14   | ... |  a0,0   |  <- Row 0
    // |  a1,15   |  a1,14   | ... |  a1,0   |  <- Row 1
    // |  a2,15   |  a2,14   | ... |  a2,0   |  <- Row 2
    // |  a3,15   |  a3,14   | ... |  a3,0   |  <- Row 3

    // Extract rows
    li t0, 0xFFFF     // Mask
    and a0, s1, t0    // Row0: lower 16 bits of block_L1
    srli a1, s1, 16   // Row1: upper 16 bits of block_L1
    and a1, a1, t0

    and a2, s2, t0    // Row2: lower 16 bits of block_L2
    srli a3, s2, 16   // Row3: upper 16 bits of block_L2
    and a3, a3, t0

    // SubColumn

    // 1. T1 = ~A1
    not t1, a1
    and t1, t1, t0

    // 2. T2 = A0 & T1
    and t2, a0, t1
    and t2, t2, t0

    // 3. T3 = A2 ^ A3
    xor t3, a2, a3
    and t3, t3, t0

    // 4. B0 = T2 ^ T3
    xor s3, t2, t3      # B0 -> s3
    and s3, s3, t0

    // 5. T5 = A3 | T1
    or t5, a3, t1
    and t5, t5, t0

    // 6. T6 = A0 ^ T5
    xor t6, a0, t5
    and t6, t6, t0

    // 7. B1 = A2 ^ T6
    xor s4, a2, t6      # B1 -> s4
    and s4, s4, t0

    // 8. T8 = A1 ^ A2
    xor t1, a1, a2      # T8 -> t1
    and t1, t1, t0

    // 9. T9 = T3 & T6
    and t2, t3, t6      # T9 -> t2
    and t2, t2, t0

    // 10. B3 = T8 ^ T9
    xor s6, t1, t2      # B3 -> s6
    and s6, s6, t0

    // 11. T11 = B0 | T8
    or t3, s3, t1       # T11 in t3
    and t3, t3, t0

    // 12. B2 = T6 ^ T11
    xor s5, t6, t3     # B4 -> s5
    and s5, s5, t0


    // ---- ShiftRow ----

    // C0 = B0 (no shift)
    // already in s3, nothing to do
    
    // C1 = B1 <<< 1
    slli t1, s4, 1
    srli t2, s4, 15
    or   s4, t1, t2
    and s4, s4, t0  // mask to 16 bits

    // C2 = B2 <<< 12
    slli t1, s5, 12
    srli t2, s5, 4
    or   s5, t1, t2
    and s5, s5, t0  // mask to 16 bits

    // C3 = B3 <<< 13
    slli t1, s6, 13
    srli t2, s6, 3
    or   s6, t1, t2
    and s6, s6, t0  // mask to 16 bits


    // Pack Row1 and Row0 into result_L1
    slli a0, s4, 16  // shift Row1 to upper half
    or a0, a0, s3    // combine with Row0

    // Pack Row3 and Row2 into result_L2
    slli a1, s6, 16  // shift Row3 to upper half
    or a1, a1, s5    // combine with Row2

    # Store packed result
    la t0, result_L1
    sw a0, 0(t0)     # result_L1
    sw a1, 4(t0)     # result_L2

    ret
