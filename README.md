# TEE Blockchain
This project is a simple demonstration of a testing environment for Trusted Execution Environment (TEE) based blockchain data collection. It aims to simulate the process of collecting data securely and verifying its integrity using TEE principles. 

## Project Structure

```
tee-blockchain
├── src
│   ├── main.ts          # Entry point of the application
│   ├── DataCollector.cpp      # TEE Enclave data collector code
│   ├── RemoteAttestation.cpp       # TEE Enclave remote attestation code
│   ├── RemoteAttestation.h       # TEE Enclave remote attestation header
│   └── types
│       └── index.ts     # Type definitions for data collection and verification
├── Enclave
│   ├── Enclave_t.c     # TEE Enclave code
│   ├── Enclave_t.h      # TEE Enclave header
│   ├── Enclave.cpp        # TEE Enclave assembly code
│   ├── tls_server.c     # TEE Enclave TLS server code
│   ├── aes.cpp       # TEE Enclave AES code
├── bank_transaction.json      # TEE Enclave bank transaction data
├── check_permissions.sol       # TEE Enclave check permissions contract code
├── check_transaction.py       # TEE Enclave check transaction code
├── data.py                  # TEE Enclave data code
├── package-lock.json      # TEE Enclave package lock file
├── package.json      # TEE Enclave package file
├── tee_blockchain_bridge.py       # TEE Enclave bridge code
├── test_connection.py        # TEE Enclave test connection code
├── test_contract.py        # TEE Enclave test contract code
├── tsconfig.json        # TEE Enclave TypeScript configuration file
└── README.md            # TEE Enclave Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/tee-blockchain.git
   cd tee-blockchain
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Compile TypeScript files:**
   ```
   npm run build
   ```

4. **Run the application:**
   ```
   npm start
   ```

## Usage

1. **Data Collection:**
   - The application simulates data collection from a TEE-enclave.
   - It collects data securely and verifies its integrity using TEE principles.

2. **Data Verification:**
   - The application verifies the integrity of the collected data.
   - It ensures that the data has not been tampered with during transit.

3. **TEE Enclave:**
   - The TEE Enclave is responsible for data collection and verification.
   - It ensures that data is processed within the Trusted Execution Environment.

4. **TEE Enclave Bridge:**
   - The TEE Enclave bridge is responsible for data transfer between the TEE Enclave and the application.
   - It ensures that data is encrypted and decrypted within the TEE Enclave.

5. **TEE Enclave Test:**
   - The TEE Enclave test is responsible for testing the TEE Enclave.
   - It ensures that the TEE Enclave is working as expected.

6. **TEE Enclave Bridge Test:**
   - The TEE Enclave bridge test is responsible for testing the TEE Enclave bridge.
   - It ensures that the TEE Enclave bridge is working as expected.


## Purpose
This project is intended for educational and testing purposes. It demonstrates the principles of TEE-based data collection and verification. It also demonstrates the principles of TEE-based contract deployment and verification. It also demonstrates the principles of TEE-based contract execution and verification.
