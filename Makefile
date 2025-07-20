SGX_SDK ?= /opt/intel/sgxsdk
SGX_MODE ?= SIM
SGX_ARCH ?= x64

include $(SGX_SDK)/buildenv.mk

App_Name := app
Enclave_Name := enclave

all: $(App_Name) $(Enclave_Name)

.PHONY: all clean

clean:
    rm -f $(App_Name) $(Enclave_Name)