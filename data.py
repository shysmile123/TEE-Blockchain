import json
from datetime import datetime, timedelta
import random
import hashlib
import string

def generate_account_id():
    """生成19位的银行账号"""
    return ''.join(random.choices(string.digits, k=19))

def generate_id_number():
    """生成18位身份证号"""
    # 随机生成省份代码(11-65)
    province = random.randint(11, 65)
    # 随机生成年月日(1960-2000)
    year = random.randint(1960, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    # 随机生成序列号
    sequence = random.randint(100, 999)
    # 随机生成校验码
    check = random.choice('0123456789X')
    return f"{province:02d}0101{year:04d}{month:02d}{day:02d}{sequence:03d}{check}"

def generate_phone():
    """生成11位手机号"""
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices(string.digits, k=8))
    return prefix + suffix

def generate_name():
    """生成随机中文姓名"""
    surnames = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张"
    names = "世永书华明志建东洪水林李月明永志建国洪"
    surname = random.choice(surnames)
    name_length = random.randint(1, 2)
    name = ''.join(random.choices(names, k=name_length))
    return surname + name

def generate_transaction_data(num_records=100):
    """生成交易数据"""
    current_time = datetime.now()
    records = []
    
    # 首先生成账户信息池
    accounts = []
    for _ in range(num_records // 2):  # 创建足够多的账户用于交易
        account = {
            "account_id": generate_account_id(),
            "name": generate_name(),
            "id_number": generate_id_number(),
            "phone": generate_phone(),
            "balance": round(random.uniform(1000, 1000000), 2)
        }
        accounts.append(account)
    
    # 生成交易记录
    for i in range(num_records):
        # 随机选择转出和转入账户
        from_account = random.choice(accounts)
        to_account = random.choice(accounts)
        while to_account == from_account:
            to_account = random.choice(accounts)
            
        # 生成交易金额
        max_amount = min(from_account["balance"], 50000)  # 设置单笔最大限额
        amount = round(random.uniform(100, max_amount), 2)
        
        # 生成交易时间
        transaction_time = current_time - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        # 生成交易记录
        transaction = {
            "transaction_id": hashlib.sha256(f"{i}".encode()).hexdigest()[:32],
            "timestamp": transaction_time.strftime("%Y-%m-%d %H:%M:%S"),
            "from_account": {
                "account_id": from_account["account_id"],
                "name": from_account["name"],
                "id_number": from_account["id_number"],
                "phone": from_account["phone"]
            },
            "to_account": {
                "account_id": to_account["account_id"],
                "name": to_account["name"],
                "id_number": to_account["id_number"],
                "phone": to_account["phone"]
            },
            "amount": amount,
            "status": "SUCCESS",
            "transaction_type": "TRANSFER",
            "description": "普通转账"
        }
        
        # 更新账户余额
        from_account["balance"] -= amount
        to_account["balance"] += amount
        
        records.append(transaction)
    
    # 按时间排序
    records.sort(key=lambda x: x["timestamp"])
    return records

# 生成数据
transactions = generate_transaction_data(100)

# 将数据保存为JSON文件
with open('bank_transactions.json', 'w', encoding='utf-8') as f:
    json.dump(transactions, f, ensure_ascii=False, indent=2)

# 打印示例数据
print(json.dumps(transactions[0], ensure_ascii=False, indent=2))