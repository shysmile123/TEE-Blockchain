from web3 import Web3
import json

def test_contract():
    print("开始测试合约连接...")
    
    # 合约地址
    CONTRACT_ADDRESS = "0x2EDa61e42cBd57DE112845588a0110a2338b0af6"
    
    # 合约ABI
    CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_address",
				"type": "address"
			}
		],
		"name": "addAuthorizedAddress",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_transactionId",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_fromAccount",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_toAccount",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_status",
				"type": "string"
			}
		],
		"name": "processTransaction",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "transactionId",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "fromAccount",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "toAccount",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "TransactionProcessed",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "authorizedAddresses",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_transactionId",
				"type": "string"
			}
		],
		"name": "getTransaction",
		"outputs": [
			{
				"internalType": "string",
				"name": "transactionId",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "fromAccount",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "toAccount",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "processedTransactions",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "transactions",
		"outputs": [
			{
				"internalType": "string",
				"name": "transactionId",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "fromAccount",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "toAccount",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
] # 从Remix复制的ABI
    
    try:
        web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        print("Web3连接状态:", web3.is_connected())
        
        # 验证合约地址
        print("合约地址:", CONTRACT_ADDRESS)
        print("是否有效地址:", Web3.is_address(CONTRACT_ADDRESS))
        
        # 尝试加载合约
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        print("合约加载成功")
        
        # 尝试调用合约方法
        owner = contract.functions.owner().call()
        print("合约拥有者:", owner)
        
    except Exception as e:
        print("测试过程中发生错误:", str(e))

if __name__ == "__main__":
    test_contract()