#include "sgx_urts.h"
#include "sgx_uae_service.h"
#include "sgx_uae_quote.h"
#include "sgx_quote.h"
#include "sgx_report.h"
#include <stdio.h>
#include <string>
#include <memory>
#include <stdexcept>
#include <json/json.h>
#include "Enclave_u.h"
#include "RemoteAttestation.h"

// 定义常量和错误码
constexpr const char* ENCLAVE_FILE = "enclave.signed.so";
constexpr size_t MAX_FILE_SIZE = 1024 * 1024 * 10; // 10MB限制

// 远程认证状态的详细定义
enum class AttestationStatus {
    SUCCESS = 0,
    PLATFORM_NOT_SUPPORTED = -1,
    ATTESTATION_FAILED = -2,
    CONNECTION_ERROR = -3,
    INVALID_PARAMETERS = -4
};

// 自定义异常类
class AttestationException : public std::runtime_error {
public:
    explicit AttestationException(const std::string& message) 
        : std::runtime_error(message) {}
};

class RemoteAttestation {
private:
    sgx_spid_t spid;
    sgx_quote_t quote;
    sgx_report_t report;
    bool is_initialized;
    
    // 验证SPID的有效性
    bool validateSpid() const {
        // 实现SPID验证逻辑
        return true; // 示例实现
    }

public:
    RemoteAttestation() : is_initialized(false) {
        memset(&spid, 0, sizeof(sgx_spid_t));
        memset(&quote, 0, sizeof(sgx_quote_t));
        memset(&report, 0, sizeof(sgx_report_t));
    }
    
    AttestationStatus initialize() {
        if (!validateSpid()) {
            return AttestationStatus::INVALID_PARAMETERS;
        }
        
        sgx_status_t status = sgx_get_quote(&report, &quote);
        if (status != SGX_SUCCESS) {
            return AttestationStatus::ATTESTATION_FAILED;
        }
        
        is_initialized = true;
        return AttestationStatus::SUCCESS;
    }
    
    bool generateAttestationReport(sgx_enclave_id_t eid) {
        if (!is_initialized) {
            throw AttestationException("Attestation not initialized");
        }
        
        sgx_status_t status = sgx_create_report(eid, &report);
        if (status != SGX_SUCCESS) {
            throw AttestationException("Failed to create attestation report");
        }
        return true;
    }
    
    bool verifyAttestation(const uint8_t* attestation_data, size_t data_size) {
        if (!attestation_data || data_size == 0) {
            throw AttestationException("Invalid attestation data");
        }
        // 实现完整的验证逻辑
        return true;
    }
};

class DataCollector {
private:
    sgx_enclave_id_t eid;
    Json::Value root;
    std::unique_ptr<RemoteAttestation> attestation;
    bool is_initialized;
    
    // 验证JSON数据的完整性
    bool validateJsonData() const {
        if (root.isNull() || !root.isObject()) {
            return false;
        }
        // 添加更多的数据验证逻辑
        return true;
    }

public:
    DataCollector() : eid(0), is_initialized(false) {
        try {
            attestation = std::make_unique<RemoteAttestation>();
            
            // 初始化SGX enclave
            sgx_status_t ret = sgx_create_enclave(
                ENCLAVE_FILE, 
                SGX_DEBUG_FLAG, 
                NULL, 
                NULL, 
                &eid, 
                NULL
            );
            
            if (ret != SGX_SUCCESS) {
                throw std::runtime_error("Enclave creation failed");
            }
            
            // 初始化远程认证
            if (attestation->initialize() != AttestationStatus::SUCCESS) {
                throw AttestationException("Remote attestation initialization failed");
            }
            
            // 生成认证报告
            if (!attestation->generateAttestationReport(eid)) {
                throw AttestationException("Failed to generate attestation report");
            }
            
            is_initialized = true;
        }
        catch (const std::exception& e) {
            fprintf(stderr, "Initialization error: %s\n", e.what());
            throw; // 重新抛出异常以通知调用者
        }
    }
    
    bool loadTransactionData(const std::string& filename) {
        if (!is_initialized) {
            throw std::runtime_error("DataCollector not properly initialized");
        }
        
        // 检查文件大小
        FILE* file = fopen(filename.c_str(), "rb");
        if (!file) {
            throw std::runtime_error("Failed to open file: " + filename);
        }
        
        fseek(file, 0, SEEK_END);
        size_t file_size = ftell(file);
        fclose(file);
        
        if (file_size > MAX_FILE_SIZE) {
            throw std::runtime_error("File size exceeds maximum allowed size");
        }
        
        // 使用RAII方式打开和读取文件
        std::ifstream json_file(filename);
        if (!json_file.is_open()) {
            throw std::runtime_error("Failed to open file: " + filename);
        }
        
        Json::CharReaderBuilder builder;
        std::string errors;
        if (!Json::parseFromStream(builder, json_file, &root, &errors)) {
            throw std::runtime_error("JSON parsing failed: " + errors);
        }
        
        return validateJsonData();
    }
    
    bool processTransaction() {
        if (!is_initialized) {
            throw std::runtime_error("DataCollector not properly initialized");
        }
        
        try {
            // 在处理数据前验证远程认证状态
            uint8_t dummy_data[] = {0x01, 0x02, 0x03}; // 示例数据
            if (!attestation->verifyAttestation(dummy_data, sizeof(dummy_data))) {
                throw AttestationException("Attestation verification failed");
            }
                     
            return true;
        }
        catch (const std::exception& e) {
            fprintf(stderr, "Transaction processing error: %s\n", e.what());
            return false;
        }
    }
    
    ~DataCollector() {
        if (eid != 0) {
            sgx_destroy_enclave(eid);
        }
    }
    
    // 禁用拷贝构造和赋值操作
    DataCollector(const DataCollector&) = delete;
    DataCollector& operator=(const DataCollector&) = delete;
};

int main() {
    try {
        DataCollector collector;
        
        if (!collector.loadTransactionData("bank_transactions.json")) {
            fprintf(stderr, "Failed to load transaction data\n");
            return -1;
        }
        
        if (!collector.processTransaction()) {
            fprintf(stderr, "Transaction processing failed\n");
            return -1;
        }
        
        printf("Transaction processed successfully\n");
        return 0;
    }
    catch (const std::exception& e) {
        fprintf(stderr, "Fatal error: %s\n", e.what());
        return -1;
    }
}