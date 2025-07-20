const Web3 = require('web3');
const fs = require('fs');
const path = require('path');

const contractPath = path.resolve(__dirname, '../contracts/BankTransactionProcessor.sol');
const contractSource = fs.readFileSync(contractPath, 'utf8');

const compiledContract = JSON.parse(solc.compile(JSON.stringify({
    language: 'Solidity',
    sources: {
        'BankTransactionProcessor.sol': {
            content: contractSource
        }
    },
    settings: {
        outputSelection: {
            '*': {
                '*': ['*']
            }
        }
    }
})));

const abi = compiledContract.contracts['BankTransactionProcessor.sol'].BankTransactionProcessor.abi;
const bytecode = compiledContract.contracts['BankTransactionProcessor.sol'].BankTransactionProcessor.evm.bytecode.object;

async function deploy() {
    if (window.ethereum) {
        const web3 = new Web3(window.ethereum);
        try {
            await window.ethereum.enable();
            const accounts = await web3.eth.getAccounts();
            const result = await new web3.eth.Contract(abi)
                .deploy({ data: '0x' + bytecode })
                .send({ from: accounts[0], gas: '3000000' });

            console.log('Contract deployed to:', result.options.address);
        } catch (error) {
            console.error('Error deploying contract:', error);
        }
    } else {
        console.error('MetaMask is not installed');
    }
}

deploy();