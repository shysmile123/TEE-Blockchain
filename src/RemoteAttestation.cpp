#include "RemoteAttestation.h"
#include <curl/curl.h>
#include <iostream>

RemoteAttestation::RemoteAttestation() : eid(0) {
    // 初始化认证数据结构
    memset(&attData, 0, sizeof(AttestationData));
    
    // 设置IAS服务的URL和访问密钥
    iasURL = "https://api.trustedservices.intel.com/sgx/dev";
    iasKey = "YOUR_IAS_PRIMARY_KEY";  
}

RemoteAttestation::~RemoteAttestation() {
    if (attData.quoteBuffer) {
        free(attData.quoteBuffer);
    }
}

AttestationStatus RemoteAttestation::initialize(sgx_enclave_id_t enclaveId) {
    eid = enclaveId;
    
    // 验证平台是否支持SGX
    if (!validatePlatform()) {
        std::cout << "Platform does not support SGX" << std::endl;
        return AttestationStatus::PLATFORM_NOT_SUPPORTED;
    }

    // 初始化Quote生成环境
    sgx_status_t ret = sgx_init_quote(&attData.targetInfo, nullptr);
    if (ret != SGX_SUCCESS) {
        std::cout << "Failed to initialize quote generation" << std::endl;
        return AttestationStatus::ATTESTATION_FAILED;
    }

    return AttestationStatus::SUCCESS;
}

AttestationStatus RemoteAttestation::generateReport() {
    // 准备报告数据
    sgx_report_data_t reportData = {0};
    sgx_status_t ret;
    
    // 在Enclave中生成报告
    ret = sgx_create_report(eid, &attData.targetInfo, &reportData, &attData.report);
    if (ret != SGX_SUCCESS) {
        std::cout << "Failed to generate report" << std::endl;
        return AttestationStatus::ATTESTATION_FAILED;
    }

    return AttestationStatus::SUCCESS;
}

AttestationStatus RemoteAttestation::getQuote() {
    // 获取Quote大小
    uint32_t quoteSize = 0;
    sgx_status_t ret = sgx_get_quote_size(nullptr, &quoteSize);
    if (ret != SGX_SUCCESS) {
        return AttestationStatus::ATTESTATION_FAILED;
    }

    // 分配Quote缓冲区
    attData.quoteBuffer = (uint8_t*)malloc(quoteSize);
    if (!attData.quoteBuffer) {
        return AttestationStatus::ATTESTATION_FAILED;
    }
    attData.quoteSize = quoteSize;

    // 生成Quote
    ret = sgx_get_quote(&attData.report,
                       SGX_UNLINKABLE_SIGNATURE,
                       nullptr,  // SPID
                       nullptr,  // nonce
                       nullptr,  // sig_rl
                       0,       // sig_rl_size
                       nullptr, // p_qe_report
                       (sgx_quote_t*)attData.quoteBuffer,
                       quoteSize);

    if (ret != SGX_SUCCESS) {
        free(attData.quoteBuffer);
        attData.quoteBuffer = nullptr;
        return AttestationStatus::ATTESTATION_FAILED;
    }

    return AttestationStatus::SUCCESS;
}

// IAS通信的回调函数
size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

AttestationStatus RemoteAttestation::communicateWithIAS() {
    CURL *curl;
    CURLcode res;
    std::string readBuffer;
    
    // 初始化CURL
    curl = curl_easy_init();
    if (!curl) {
        return AttestationStatus::IAS_CONNECTION_FAILED;
    }

    // 设置IAS请求
    struct curl_slist *headers = nullptr;
    headers = curl_slist_append(headers, ("Ocp-Apim-Subscription-Key: " + iasKey).c_str());
    headers = curl_slist_append(headers, "Content-Type: application/json");

    // 准备Quote数据
    std::string quoteBase64;  

    // 设置CURL选项
    curl_easy_setopt(curl, CURLOPT_URL, (iasURL + "/attestation/v4/report").c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POST, 1L);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, quoteBase64.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

    // 执行请求
    res = curl_easy_perform(curl);
    
    // 清理
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK) {
        return AttestationStatus::IAS_CONNECTION_FAILED;
    }

    return AttestationStatus::SUCCESS;
}

AttestationStatus RemoteAttestation::verifyAttestation() {
    // 验证Quote签名
    sgx_quote_t* quote = (sgx_quote_t*)attData.quoteBuffer;
    
    // 验证Quote的各个字段
    if (!quote) {
        return AttestationStatus::QUOTE_VERIFICATION_FAILED;
    }

    // 验证MRENCLAVE和MRSIGNER
    // 
    return AttestationStatus::SUCCESS;
}

bool RemoteAttestation::validatePlatform() {
    int sgx_support;
    sgx_status_t ret = sgx_is_capable(&sgx_support);
    return (ret == SGX_SUCCESS && sgx_support);
}
