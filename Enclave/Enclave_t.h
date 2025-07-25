#ifndef ENCLAVE_T_H__
#define ENCLAVE_T_H__

#include <stdint.h>
#include <wchar.h>
#include <stddef.h>
#include "sgx_edger8r.h" /* for sgx_ocall etc. */


#define SGX_CAST(type, item) ((type)(item))

#ifdef __cplusplus
extern "C" {
#endif

void process_data(const char* data, size_t len);

sgx_status_t SGX_CDECL ocall_print(const char* str);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif
