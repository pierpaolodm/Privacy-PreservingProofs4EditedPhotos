[![Circom Badge](https://img.shields.io/badge/circuits-circom-black)](https://github.com/iden3/circom)
[![Snarkjs Badge](https://img.shields.io/badge/proof_system-snarkjs-yellow)](https://github.com/iden3/snarkjs)
![Python Badge](https://img.shields.io/badge/generate-python-green)
# Decentralized Zero-Knowledge Image Transformations

In the digital age, many online images are transformations of original, private content. Whether for economic value or sensitive material, maintaining the confidentiality and authenticity of the original image is crucial. Our project introduces a system designed to efficiently prove and verify the authenticity of transformed images.

## Key Objectives:

1. **Confidentiality:** Ensure the original image remains private.
2. **Efficient Proof Generation:** Enable proof computation on standard hardware.
3. **Integrity:** Confirm that only advertised transformations have been applied.
4. **Fast Fraud Detection:** Swiftly identify and reject fraudulent proofs.

Our approach employs a divide-and-conquer strategy, applying sub-transformations to tiles of the original image. These tiles are then reconnected with their sub-proofs, ensuring both efficiency and security.

In our experimental evaluation, we focus on transformations like resizing. Results demonstrate the practicality of our approach, showcasing the generation of a faithful transformation for a 30MP high-resolution image with minimal hardware requirements: 16GB of RAM and 8 cores in just over 45 minutes.

## Requirements
### For Python:

- **numpy** v1.26.2
- **opencv_python** v4.8.1.78
- **tensorflow_cpu** v2.14.0

### Other Requirements:

- Install **circom**
- Install **snarkjs**
- Install **rapidsnark**

Make sure to obtain a `poweroftau`.

## Getting Started:

1.  Clone this repository to your local system.
2.  Run `generate_proof.py`

