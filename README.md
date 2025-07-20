# A Trusted IoT Data Collection Scheme Based on TEE and Blockchain

This project demonstrates a secure data collection and testing environment for IoT devices using Trusted Execution Environment (TEE) and blockchain. The system enables TEE to **actively fetch smart contracts**, verify their integrity, and ensure trusted data reporting.

## 🧠 Overview

- **TEE (Trusted Execution Environment)** is used to collect and process IoT data securely.
- The **Blockchain** stores smart contracts and verifies data integrity.
- The TEE actively retrieves and interacts with smart contracts through a secure remote attestation mechanism.

## 📁 Project Structure

```
tee-blockchain/
├── src/
│   ├── main.ts                         # Entry point of the application
│   ├── DataCollector.cpp               # TEE Enclave data collector
│   ├── RemoteAttestation.cpp/.h        # TEE Enclave remote attestation
│   └── types/index.ts                  # Type definitions for data collection
│
├── Enclave/
│   ├── Enclave_t.c / Enclave_t.h       # TEE Enclave trusted components
│   ├── Enclave.cpp                     # TEE Enclave application logic
│   ├── tls_server.c                    # TLS server for secure communication
│   └── aes.cpp                         # AES encryption logic
│
├── contracts/
│   ├── check_permissions.sol           # Solidity smart contract for permission checks
│
├── test_contract.py                    # Python contract interaction tester
├── test_connection.py                 # Python TEE connection tester
├── tee_blockchain_bridge.py           # Bridge between TEE and blockchain
├── data.py                             # Simulation dataset handler
├── bank_transactions.json              # Sample IoT data in JSON
├── package.json / package-lock.json    # Node.js configs
├── tsconfig.json                       # TypeScript compiler config
└── README.md                           # Project documentation
```

## ✅ Features

- **Remote Attestation**: Verifies smart contracts before execution.
- **Active Contract Retrieval**: TEE fetches contracts dynamically.
- **Secure Data Channel**: TLS encrypted transmission with AES support.
- **Cross-Chain Compatibility**: Designed to interact with EVM-based blockchains.

## ⚙️ Build & Run

```bash
# Compile Enclave
make

# Install dependencies
npm install

# Start backend interface
npm run start


## Purpose
This project is intended for educational and testing purposes. It demonstrates the principles of TEE-based data collection and verification. It also demonstrates the principles of TEE-based contract deployment and verification. It also demonstrates the principles of TEE-based contract execution and verification.
