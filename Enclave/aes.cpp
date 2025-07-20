#include <openssl/aes.h>

void encryptSensitiveData(const std::string& plaintext, std::string& ciphertext, const std::string& key) {
    AES_KEY encrypt_key;
    unsigned char iv[AES_BLOCK_SIZE] = {0}; // 初始化IV为0（可以根据实际需求改变）
    
    // 设置加密密钥
    AES_set_encrypt_key(reinterpret_cast<const unsigned char*>(key.c_str()), 128, &encrypt_key);
    
    // 分配内存用于存储加密后的数据
    unsigned char* enc_data = new unsigned char[plaintext.size()];
    
    // 执行加密操作
    AES_cbc_encrypt(reinterpret_cast<const unsigned char*>(plaintext.c_str()), enc_data, plaintext.size(), &encrypt_key, iv, AES_ENCRYPT);
    
    ciphertext.assign(reinterpret_cast<char*>(enc_data), plaintext.size());
    delete[] enc_data;
}
