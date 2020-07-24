# -*- coding: utf-8 -*-
import ctypes
import sys

from common.error import MyError


class LDKHelper:
    def __init__(self, sVendorCode,soPath):
        self.pStrVendorCode = ctypes.c_char_p()
        self.pStrVendorCode.value = sVendorCode.encode()
        self.soPath = soPath
        if soPath == "":
            self.soPath = "/home/lynxi/lockDemo/LDK_Runtime_API_Python_Sample/lib/x86_64/libhasp_linux_x86_64_demo.so"
        self.so = ctypes.CDLL(self.soPath)

        # Configure the scope of hasp_get_info call. In this sample, all accessible keys are listed.
        self.pAccessibleKeyScope = ctypes.c_char_p()
        sAccessibleKeyScope = '<?xml version=\"1.0\" encoding=\"UTF-8\" ?>' \
                              '<haspscope/>'
        self.pAccessibleKeyScope.value = sAccessibleKeyScope.encode()

        # Configure the format of hasp_get_info call. In this sample, key id and key type are listed.
        self.pAccessibleKeyFormat = ctypes.c_char_p()
        sAccessibleKeyFormat = '<?xml version=\"1.0\" encoding=\"UTF-8\" ?>' \
                               '<haspformat root=\"hasp_info\">' \
                               '<hasp>' \
                               '<attribute name=\"id\" />' \
                               '<attribute name=\"type\" />' \
                               '</hasp>' \
                               '</haspformat>'
        self.pAccessibleKeyFormat.value = sAccessibleKeyFormat.encode()

        # Configure the format of hasp_get_sessioninfo call. In this sample, key info are listed.
        self.pStrInfo = ctypes.c_char_p()
        self.pStrKeyInfoFormat = ctypes.c_char_p()
        sKeyInfoFormat = '<haspformat format=\"keyinfo\"/>'
        self.pStrKeyInfoFormat.value = sKeyInfoFormat.encode()

        self.handle = ctypes.c_uint32()

        # Change the feature id to the features contained in your protection key.
        self.intFeatureId = ctypes.c_uint32(0)
        self.intReturnStatus = ctypes.c_uint32()

        # Change offset and length based on the data in your protection key.
        self.intMemoryOffset = ctypes.c_uint32(0)
        self.intMemoryLength = ctypes.c_uint32(64)
        self.intFileIdRO = ctypes.c_uint32(65525)
        self.intFileIdRW = ctypes.c_uint32(65524)
        self.pIntMemorySize = ctypes.c_uint32()
        self.sMemoryData = (ctypes.c_char * 64)()
        self.aCharMemoryWriteData = (ctypes.c_char * 64)()

        # Data to be encrypted by hasp_encrypt call.
        self.aCharEncryptionData = (ctypes.c_char * 64)()

    def login(self):
        self.__hasp_get_info__()
        self.so.hasp_login(self.intFeatureId, self.pStrVendorCode, ctypes.byref(self.handle))
        if self.intReturnStatus != 0:
            print("Login failed")
            if self.intReturnStatus == 7:
                print("Sentinel protection key not found")
                raise MyError(10006, "Sentinel protection key not found")
                sys.exit(0)
            elif self.intReturnStatus == 22:
                print("Invalid Vendor Code was passed")
                raise MyError(10007, "Invalid Vendor Code was passed")
                sys.exit(0)
            elif self.intReturnStatus == 31:
                print("Requested Feature not found")
                raise MyError(10008, "Requested Feature not found")
                sys.exit(0)
            else:
                print("Error code:", self.intReturnStatus)
                raise MyError(10009, "Error code:", self.intReturnStatus)
                sys.exit(0)
        else:
            print("Login success")
        pass

    def read_data(self):
        self.intReturnStatus = self.so.hasp_read(self.handle,
                                                 self.intFileIdRW,
                                                 self.intMemoryOffset,
                                                 self.intMemoryLength,
                                                 self.sMemoryData)
        if self.intReturnStatus != 0:
            print("Get RW memory data failed")
            if self.intReturnStatus == 9:
                print("Invalid handle was passed to function")
                raise MyError(10010, "Invalid handle was passed to function")
            elif self.intReturnStatus == 10:
                print("Specified File ID is not recognized by API")
                raise MyError(10011, "Specified File ID is not recognized by API")
            elif self.intReturnStatus == 1:
                print("Request exceeds the Sentinel protection key memory range")
                raise MyError(10012, "Request exceeds the Sentinel protection key memory range")
            else:
                print("Error code:", self.intReturnStatus)
                raise MyError(10013, "Error code:", self.intReturnStatus)
        else:
            print(self.sMemoryData.value.decode('utf-8'))
            return self.sMemoryData.value.decode('utf-8')

    def write_data(self,data):
        # sMemoryWriteData = 'This is data stored in RW memory modified by write API call'
        sMemoryWriteData = data
        self.aCharMemoryWriteData.value = sMemoryWriteData.encode()
        self.intReturnStatus = self.so.hasp_write(self.handle,
                                                  self.intFileIdRW,
                                                  self.intMemoryOffset,
                                                  self.intMemoryLength,
                                                  self.aCharMemoryWriteData)
        if self.intReturnStatus != 0:
            print("Modify RW memory data failed")
            if self.intReturnStatus == 9:
                print("Invalid handle was passed to function")
                raise MyError(10014, "Invalid handle was passed to function")
            elif self.intReturnStatus == 10:
                print("Specified File ID is not recognized by API")
                raise MyError(10015, "Specified File ID is not recognized by API")
            elif self.intReturnStatus == 1:
                print("Request exceeds the Sentinel protection key memory range")
                raise MyError(10016, "Request exceeds the Sentinel protection key memory range")
            else:
                print("Error code:", self.intReturnStatus)
                raise MyError(10017, "Error code:", self.intReturnStatus)
        else:
            print("RW memory modified")

    def encrypt_data(self,data):
        sEncryptionText = data
        self.aCharEncryptionData.value = sEncryptionText.encode()
        self.intReturnStatus = self.so.hasp_encrypt(self.handle, self.aCharEncryptionData, self.intMemoryLength)
        if self.intReturnStatus != 0:
            print("Data encryption failed")
            if self.intReturnStatus == 9:
                print("Invalid handle was passed to function")
                raise MyError(10018, "Invalid handle was passed to function")
            elif self.intReturnStatus == 8:
                print("Encrypted/decrypted data length too short to execute function call")
                raise MyError(10019, "Encrypted/decrypted data length too short to execute function call")
            elif self.intReturnStatus == 23:
                print("Sentinel protection key does not support encryption type")
                raise MyError(10020, "Sentinel protection key does not support encryption type")
            else:
                print("Error code:", self.intReturnStatus)
                raise MyError(10021, "Error code:", self.intReturnStatus)
        else:
            print("Data after encryption:", self.aCharEncryptionData.value)
            return self.aCharEncryptionData.value

    def decrypt_data(self):
        self.intReturnStatus = self.so.hasp_decrypt(self.handle, self.aCharEncryptionData, self.intMemoryLength)
        if self.intReturnStatus != 0:
            print("Data decryption failed")
            if self.intReturnStatus == 9:
                print("Invalid handle was passed to function")
                raise MyError(10022, "Invalid handle was passed to function")
            elif self.intReturnStatus == 8:
                print("Encrypted/decrypted data length too short to execute function call")
                raise MyError(10023, "Encrypted/decrypted data length too short to execute function call")
            elif self.intReturnStatus == 23:
                print("Sentinel protection key does not support encryption type")
                raise MyError(10024, "Sentinel protection key does not support encryption type")
            else:
                print("Error code:", self.intReturnStatus)
                raise MyError(10025, "Error code:", self.intReturnStatus)
        else:
            print("Data after decryption:", self.aCharEncryptionData.value)
            return self.aCharEncryptionData.value

    def logout(self):
        self.intReturnStatus = self.so.hasp_logout(self.handle)
        if self.intReturnStatus != 0:
            print("Logout failed")
            if self.intReturnStatus == 9:
                print("Invalid handle was passed to function")
                raise MyError(10026, "Invalid handle was passed to function")
            else:
                print("Error code:", self.intReturnStatus)
                raise MyError(10027, "Error code:", self.intReturnStatus)
        else:
            print("Logout success")

    def __hasp_get_info__(self):
        self.intReturnStatus = self.so.hasp_get_info(self.pAccessibleKeyScope,
                                                     self.pAccessibleKeyFormat,
                                                     self.pStrVendorCode,
                                                     ctypes.byref(self.pStrInfo))
        if self.intReturnStatus != 0:
            print("Get accessible keys failed")
            if self.intReturnStatus == 9:
                print("Invalid handle was passed to function")
                raise MyError(10001, "Invalid handle was passed to function")
                sys.exit(0)
            elif self.intReturnStatus == 15:
                print("Format is not recognized")
                raise MyError(10002, "Format is not recognized")
                sys.exit(0)
            elif self.intReturnStatus == 36:
                print("Invalid XML scope exists")
                raise MyError(10003, "Invalid XML scope exists")
                sys.exit(0)
            elif self.intReturnStatus == 50:
                print("Unable to locate any key that matches the scope")
                raise MyError(10004, "Unable to locate any key that matches the scope")
                sys.exit(0)
            else:
                print("Error code:", self.intReturnStatus)
                raise MyError(10005, "Error code:", self.intReturnStatus)
                sys.exit(0)
        else:
            print("Accessible keys are listed:")
            print(self.pStrInfo.value.decode('utf-8'))
