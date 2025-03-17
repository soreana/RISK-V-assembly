


Since there is no publicly available Python implementation of the RECTANGLE block cipher, I used the JavaScript implementation available on GitHub [1] as a reference to ensure that my Python and RISC-V assembly implementations adhere to the original algorithm's design. All cryptographic operations, including the S-box, ShiftRow, and key addition, were cross-verified with the JavaScript code to ensure correctness.
[1] m-walid, "Rectangle-lightweight-block-cipher," GitHub repository, https://github.com/m-walid/Rectangle-lightweight-block-cipher
