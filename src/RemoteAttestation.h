#pragma once
#include <string>
#include "sgx_urts.h"
#include "sgx_quote.h"
#include "sgx_report.h"
#include "sgx_uae_service.h"
#include "sgx_utils.h"

// 定义远程认证的状态枚举
enum class AttestationStatus {
    SUCCESS,
    PLATFORM_NOT_SUPPORTED,
    ATTESTATION_FAILED,
    CONNECTION_ERROR,
    IAS_CONNECTION_FAILED,
    QUOTE_VERIFICATION_FAILED
};

// 定义认证数据结构
struct AttestationData {
    sgx_target_info_t targetInfo;
    sgx_report_t report;
    sgx_quote_t* quote;
    uint8_t* quoteBuffer;
    uint32_t quoteSize;
};

class RemoteAttestation {
public:
    RemoteAttestation();
    ~RemoteAttestation();

    // 初始化远程认证环境
    AttestationStatus initialize(sgx_enclave_id_t enclaveId);
    // 生成认证报告
    AttestationStatus generateReport();
    // 获取认证引用
    AttestationStatus getQuote();
    // 验证认证状态
    AttestationStatus verifyAttestation();
    // 与IAS服务通信
    AttestationStatus communicateWithIAS();

private:
    sgx_enclave_id_t eid;
    AttestationData attData;
    std::string iasURL;
    std::string iasKey;

    // 内部辅助函数
    bool initializeEnclave();
    bool validatePlatform();
    bool prepareQuoteGeneration();
};