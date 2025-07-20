// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BankTransactionProcessor {
    // 定义交易数据结构
    struct Transaction {
        string transactionId;
        uint256 timestamp;
        string fromAccount;
        string toAccount;
        uint256 amount;
        string status;
    }
    
    // 存储交易记录
    mapping(string => Transaction) public transactions;
    // 存储已处理的交易ID
    mapping(string => bool) public processedTransactions;
    // 授权地址
    mapping(address => bool) public authorizedAddresses;
    
    // 事件
    event TransactionProcessed(
        string transactionId,
        string fromAccount,
        string toAccount,
        uint256 amount
    );
    
    // 合约拥有者
    address public owner;
    
    constructor() {
        owner = msg.sender;
        authorizedAddresses[msg.sender] = true;
    }
    
    // 仅授权地址可调用
    modifier onlyAuthorized() {
        require(authorizedAddresses[msg.sender], "Not authorized");
        _;
    }
    
    // 添加授权地址
    function addAuthorizedAddress(address _address) public {
        require(msg.sender == owner, "Only owner can add authorized addresses");
        authorizedAddresses[_address] = true;
    }
    
    // 处理单笔交易数据
    function processTransaction(
        string memory _transactionId,
        uint256 _timestamp,
        string memory _fromAccount,
        string memory _toAccount,
        uint256 _amount,
        string memory _status
    ) public onlyAuthorized {
        require(!processedTransactions[_transactionId], "Transaction already processed");
        
        transactions[_transactionId] = Transaction(
            _transactionId,
            _timestamp,
            _fromAccount,
            _toAccount,
            _amount,
            _status
        );
        
        processedTransactions[_transactionId] = true;
        
        emit TransactionProcessed(_transactionId, _fromAccount, _toAccount, _amount);
    }
    
    // 查询交易信息
    function getTransaction(string memory _transactionId) public view returns (
        string memory transactionId,
        uint256 timestamp,
        string memory fromAccount,
        string memory toAccount,
        uint256 amount,
        string memory status
    ) {
        Transaction memory txn = transactions[_transactionId];
        require(processedTransactions[_transactionId], "Transaction not found");
        
        return (
            txn.transactionId,
            txn.timestamp,
            txn.fromAccount,
            txn.toAccount,
            txn.amount,
            txn.status
        );
    }
}