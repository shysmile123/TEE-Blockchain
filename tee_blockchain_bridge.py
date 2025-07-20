import json
import time
from web3 import Web3
from datetime import datetime

class TEEDataProcessor:
    def __init__(self, contract_address, contract_abi, web3_provider="http://127.0.0.1:8545"):
        print("初始化TEE数据处理器...")
        
        # 连接到本地以太坊节点
        try:
            self.web3 = Web3(Web3.HTTPProvider(web3_provider))
            print(f"Web3连接状态: {self.web3.is_connected()}")
        except Exception as e:
            print(f"Web3连接错误: {str(e)}")
            raise
        
        # 检查合约地址格式
        if not Web3.is_address(contract_address):
            print(f"无效的合约地址: {contract_address}")
            raise ValueError("Invalid contract address")
            
        # 加载智能合约
        try:
            self.contract = self.web3.eth.contract(
                address=contract_address,
                abi=contract_abi
            )
            print("合约加载成功")
        except Exception as e:
            print(f"合约加载错误: {str(e)}")
            raise
        
        # 设置默认账户
        try:
            self.web3.eth.default_account = self.web3.eth.accounts[0]
            print(f"使用默认账户: {self.web3.eth.default_account}")
        except Exception as e:
            print(f"设置默认账户错误: {str(e)}")
            raise

    def process_transaction_data(self, transaction):
        """处理单个交易数据"""
        try:
            print(f"\n处理交易: {transaction['transaction_id']}")
            
            # 转换时间戳
            timestamp = int(time.mktime(datetime.strptime(
                transaction["timestamp"], 
                "%Y-%m-%d %H:%M:%S"
            ).timetuple()))
            
            # 调用智能合约
            tx_hash = self.contract.functions.processTransaction(
                transaction["transaction_id"],
                timestamp,
                transaction["from_account"]["account_id"],
                transaction["to_account"]["account_id"],
                int(transaction["amount"] * 100),  # 转换为整数（分）
                transaction["status"]
            ).transact({'from': self.web3.eth.default_account, 'gas': 300000}) #防止gas不足          
            # 等待交易确认
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"交易确认，区块号: {receipt['blockNumber']}")
            return True
            
        except Exception as e:
            print(f"处理交易错误: {str(e)}")
            return False

    def process_batch_data(self, json_file_path):
        """处理JSON文件中的所有交易数据"""
        try:
            print(f"\n开始读取文件: {json_file_path}")
            with open(json_file_path, 'r', encoding='utf-8') as f:
                transactions = json.load(f)
            
            print(f"找到 {len(transactions)} 条交易记录")
            
            successful = 0
            failed = 0
            
            for transaction in transactions:
                if self.process_transaction_data(transaction):
                    successful += 1
                else:
                    failed += 1
            
            print(f"\n处理完成:")
            print(f"成功处理: {successful}")
            print(f"处理失败: {failed}")
            
        except FileNotFoundError:
            print(f"找不到文件: {json_file_path}")
        except json.JSONDecodeError:
            print("JSON文件格式错误")
        except Exception as e:
            print(f"批处理错误: {str(e)}")

# 主程序
if __name__ == "__main__":
    # 替换为部署的合约地址
    CONTRACT_ADDRESS = "0x2EDa61e42cBd57DE112845588a0110a2338b0af6"
    
    # 从Remix IDE获取的ABI
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
    ]
    
    try:
        print("启动TEE数据处理程序...")
        processor = TEEDataProcessor(CONTRACT_ADDRESS, CONTRACT_ABI)
        processor.process_batch_data("bank_transactions.json")
    except Exception as e:
        print(f"程序执行错误: {str(e)}")