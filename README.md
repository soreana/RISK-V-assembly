# Cryptographic Engineering - Project 3 - RISC-V

Welcome to the **Cryptographic Engineering** course projects repository. This repository contains multiple RISC-V Assembly implementations of lightweight cryptographic primitives, designed for educational purposes and performance analysis on embedded architectures.  

Each folder contains a separate project with its own detailed description and implementation. Please refer to the individual `README.md` files inside each project for more details.

---

## Project Structure

```
.
├── part-1-Katan32/
├── part-2-RECTANGLE/
└── CallAssembly.zip
```

---

### part-1-Katan32/

- **Description**:  
  This project contains the **RISC-V Assembly implementation of the KATAN-32 cipher**, a lightweight block cipher designed for constrained devices.
- **Contents**:  
  - Full Assembly implementation of one round of KATAN-32.
  - C code to call the assembly functions and verify results.
  - Python code to verify the result of assembly function.
- **Documentation**:  
  Please check the detailed [README.md](part-1-Katan32/README.md) inside the `part-1-Katan32` folder for setup instructions, algorithm details, and expected outputs.

---

### part-2-RECTANGLE/

- **Description**:  
  This project contains the **RISC-V Assembly implementation of a single round of the RECTANGLE block cipher**, focusing on bitsliced S-box and shift row transformations.
- **Contents**:  
  - Full Assembly implementation of one round of RECTANGLE.
  - C code to interface with the assembly and validate results.
  - C code to verify the result of assembly function.
- **Documentation**:  
  See the detailed [README.md](part-2-RECTANGLE/README.md) inside `part-2-RECTANGLE` for explanation of the algorithm, instructions to run, and sample outputs.

---

### CallAssembly.zip

- **Description**:  
  This ZIP file contains the **base project structure** shared as part of the course. It includes example files and sample on how to integrate C code with RISC-V Assembly for testing and running the cryptographic functions.

