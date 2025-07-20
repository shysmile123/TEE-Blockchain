#include "Enclave_t.h"
#include "sgx_trts.h"
#include "sgx_utils.h"
#include "src/RemoteAttestation.h" 

sgx_status_t generate_report(sgx_target_info_t* target_info, sgx_report_t* report) {
    sgx_report_data_t report_data = {0};
    
    return sgx_create_report(target_info, &report_data, report);
}

// 在主程序中使用远程认证
int main() {
    RemoteAttestation attestation;
    sgx_enclave_id_t eid;
    
    // 初始化远程认证
    AttestationStatus status = attestation.initialize(eid);
    if (status != AttestationStatus::SUCCESS) {
        // 处理错误
        return -1;
    }
    
    // 生成报告
    status = attestation.generateReport();
    if (status != AttestationStatus::SUCCESS) {
        // 处理错误
        return -1;
    }
    
    // 获取Quote
    status = attestation.getQuote();
    if (status != AttestationStatus::SUCCESS) {
        // 处理错误
        return -1;
    }
    
    // 与IAS通信
    status = attestation.communicateWithIAS();
    if (status != AttestationStatus::SUCCESS) {
        // 处理错误
        return -1;
    }
    
    // 验证认证结果
    status = attestation.verifyAttestation();
    if (status != AttestationStatus::SUCCESS) {
        // 处理错误
        return -1;
    }
    
    // 认证成功，继续处理业务逻辑
    return 0;
}


#include "Enclave_t.h"  
#include <string>
#include <fstream>
#include <sstream>
#include <json/json.h>
#include <openssl/sha.h> 

bool validateDataIntegrity(const std::string& json_data) {
    // 使用SHA256或者其他哈希算法验证数据完整性
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256_ctx;
    SHA256_Init(&sha256_ctx);
    SHA256_Update(&sha256_ctx, json_data.c_str(), json_data.size());
    SHA256_Final(hash, &sha256_ctx);
    
    return true;  // 如果验证成功返回true
}

// ECALL 接口：读取并验证数据
void readAndValidateData(const char* file_path) {
    std::ifstream file(file_path);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file");
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string json_data = buffer.str();
    
    // 验证数据完整性
    if (!validateDataIntegrity(json_data)) {
        throw std::runtime_error("Data integrity check failed");
    }
    
}
