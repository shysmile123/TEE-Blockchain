import json
from web3 import Web3

class TransactionChecker:
    def __init__(self, contract_address, contract_abi, web3_provider="http://127.0.0.1:8545"):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        if not self.web3.is_connected():
            raise Exception("无法连接到以太坊节点")
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        self.web3.eth.default_account = self.web3.eth.accounts[0]

    def check_transaction(self, transaction):
        try:
            owner = self.contract.functions.owner().call()
            print(f"合约拥有者: {owner}")
            print(f"当前账户: {self.web3.eth.default_account}")
            
            if owner.lower() == self.web3.eth.default_account.lower():
                tx_hash = self.contract.functions.addAuthorizedAddress(
                    self.web3.eth.default_account
                ).transact()
                self.web3.eth.wait_for_transaction_receipt(tx_hash)
                print("已添加授权")
        
            # 调用智能合约
            print("准备调用合约processTransaction函数...")
            tx_hash = self.contract.functions.processTransaction(
                transaction["transaction_id"],
                transaction["timestamp"],
                transaction["from_account"]["account_id"],
                transaction["to_account"]["account_id"],
                int(transaction["amount"] * 100),  # 转换为整数
                transaction["status"]
            ).transact({'from': self.web3.eth.default_account, 'gas': 300000})
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print("交易处理完成")
        except Exception as e:
            print(f"处理交易错误: {str(e)}")

# 示例调用
contract_address = "0x2EDa61e42cBd57DE112845588a0110a2338b0af6"  
contract_abi = json.loads('[{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_address","type":"address"}],"name":"addAuthorizedAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_transactionId","type":"uint256"},{"name":"_timestamp","type":"uint256"},{"name":"_fromAccount","type":"string"},{"name":"_toAccount","type":"string"},{"name":"_amount","type":"uint256"},{"name":"_status","type":"string"}],"name":"processTransaction","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"message","type":"string"},{"indexed":false,"internalType":"uint256","name":"transactionId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"string","name":"fromAccount","type":"string"},{"indexed":false,"internalType":"string","name":"toAccount","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"string","name":"status","type":"string"}],"name":"Debug","type":"event"}]')
transaction = {
    "transaction_id": 1,
    "timestamp": 1633024800,
    "from_account": {"account_id": "0xFromAccount"},
    "to_account": {"account_id": "0xToAccount"},
    "amount": 100.0,
    "status": "completed"
}

checker = TransactionChecker(contract_address, contract_abi)
checker.check_transaction(transaction)