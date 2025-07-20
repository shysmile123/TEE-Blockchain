#include <openssl/ssl.h>
#include <openssl/err.h>
#include "Enclave_t.h"

void tls_server() {
    SSL_CTX *ctx;
    SSL *ssl;
    int server_fd, client_fd;

    // Initialize OpenSSL
    SSL_load_error_strings();
    OpenSSL_add_ssl_algorithms();

    // Create SSL context
    const SSL_METHOD *method = TLS_server_method();
    ctx = SSL_CTX_new(method);
    if (!ctx) {
        printf("Unable to create SSL context\n");
        return;
    }

    // Load server certificate and private key
    if (SSL_CTX_use_certificate_file(ctx, "server.crt", SSL_FILETYPE_PEM) <= 0) {
        printf("Failed to load certificate\n");
        SSL_CTX_free(ctx);
        return;
    }
    if (SSL_CTX_use_PrivateKey_file(ctx, "server.key", SSL_FILETYPE_PEM) <= 0) {
        printf("Failed to load private key\n");
        SSL_CTX_free(ctx);
        return;
    }

    // Setup server socket
    server_fd = setup_server_socket(443);  // 自定义函数，监听 443 端口
    client_fd = accept_connection(server_fd);  // 接受客户端连接

    // Create SSL session
    ssl = SSL_new(ctx);
    SSL_set_fd(ssl, client_fd);

    if (SSL_accept(ssl) <= 0) {
        printf("SSL accept failed\n");
    } else {
        printf("TLS connection established\n");

        // Secure communication
        char buffer[1024] = {0};
        SSL_read(ssl, buffer, sizeof(buffer));
        printf("Received: %s\n", buffer);

        SSL_write(ssl, "Hello from SGX", strlen("Hello from SGX"));
    }

    // Cleanup
    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(client_fd);
    close(server_fd);
    SSL_CTX_free(ctx);
}
