from web3 import Web3
import sys
import web3

def test_environment():
    print("开始环境测试...")
    print("Python版本:", sys.version)
    print("Web3版本:", web3.__version__)  
    
    try:
        # 测试Web3连接
        web3_instance = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        print("Web3连接状态:", web3_instance.is_connected())
        
        if web3_instance.is_connected():
            print("当前区块号:", web3_instance.eth.block_number)
            print("可用账户:", web3_instance.eth.accounts)
            
        # 测试JSON文件读取
    except Exception as e:
        print("An error occurred:", e)  # 捕获并打印异常

# 调用函数
test_environment()