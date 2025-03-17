


Since there is no publicly available Python implementation of the RECTANGLE block cipher, I used the JavaScript implementation available on GitHub [1] as a reference to ensure that my Python and RISC-V assembly implementations adhere to the original algorithm's design. All cryptographic operations, including the S-box, ShiftRow, and key addition, were cross-verified with the JavaScript code to ensure correctness.
[1] m-walid, "Rectangle-lightweight-block-cipher," GitHub repository, https://github.com/m-walid/Rectangle-lightweight-block-cipher


# Cryptographic Engineering - Project 3 - RISC-V

Welcome to the **Cryptographic Engineering** course projects repository. This repository contains multiple RISC-V Assembly implementations of lightweight cryptographic primitives, designed for educational purposes and performance analysis on embedded architectures.  

Each folder contains a separate project with its own detailed description and implementation. Please refer to the individual `README.md` files inside each project for more details.

---

## 📂 Project Structure

```
.
├── part-1-Katan32/
├── part-2-RECTANGLE/
└── CallAssembly.zip
```

---

### 📁 part-1-Katan32/

- **Description**:  
  This project contains the **RISC-V Assembly implementation of the KATAN-32 cipher**, a lightweight block cipher designed for constrained devices.
- **Contents**:  
  - Full Assembly implementation of KATAN-32.
  - C code to call the assembly functions and verify results.
- **Documentation**:  
  Please check the detailed [README.md](part-1-Katan32/README.md) inside the `part-1-Katan32` folder for setup instructions, algorithm details, and expected outputs.

---

### 📁 part-2-RECTANGLE/

- **Description**:  
  This project contains the **RISC-V Assembly implementation of a single round of the RECTANGLE block cipher**, focusing on bitsliced S-box and shift row transformations.
- **Contents**:  
  - Full Assembly implementation of one round of RECTANGLE.
  - C code to interface with the assembly and validate results.
- **Documentation**:  
  See the detailed [README.md](part-2-RECTANGLE/README.md) inside `part-2-RECTANGLE` for explanation of the algorithm, instructions to run, and sample outputs.

---

### 📦 CallAssembly.zip

- **Description**:  
  This ZIP file contains the **base project structure** shared as part of the course. It includes example files and guidelines on how to integrate C code with RISC-V Assembly for testing and running the cryptographic functions.
- **Note**:  
  Please extract and review this structure if you are setting up a new project or aligning with the provided format.

---

## ✅ How to Use

1. Choose the specific cipher project you want to explore:
   - `part-1-Katan32` for KATAN-32.
   - `part-2-RECTANGLE` for RECTANGLE.
2. Follow the instructions provided in each project's `README.md`.
3. Compile and run using the provided commands and observe the output for verification.
