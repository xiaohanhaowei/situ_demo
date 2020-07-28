# -*- coding: utf-8 -*-
import base64

from Crypto.Cipher import AES

from common.error import MyError
from common.ldkhelper import LDKHelper


# 解密
def AES_Decrypt(key, data):
    vi = '0102030405060708'
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 去补位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted


# 获取加密锁中解密后的值
def GetValue():
    key, data = ReadEncryptionLock()
    value = AES_Decrypt(key, data)
    return value


# 从加密锁读取key和data
def ReadEncryptionLock():
    sVendorCode = 'AzIceaqfA1hX5wS+M8cGnYh5ceevUnOZIzJBbXFD6dgf3tBkb9cvUF/Tkd/iKu2fsg9wAysY' \
                  'Kw7RMAsVvIp4KcXle/v1RaXrLVnNBJ2H2DmrbUMOZbQUFXe698qmJsqNpLXRA367xpZ54i8k' \
                  'C5DTXwDhfxWTOZrBrh5sRKHcoVLumztIQjgWh37AzmSd1bLOfUGI0xjAL9zJWO3fRaeB0NS2' \
                  'KlmoKaVT5Y04zZEc06waU2r6AU2Dc4uipJqJmObqKM+tfNKAS0rZr5IudRiC7pUwnmtaHRe5' \
                  'fgSI8M7yvypvm+13Wm4Gwd4VnYiZvSxf8ImN3ZOG9wEzfyMIlH2+rKPUVHI+igsqla0Wd9m7' \
                  'ZUR9vFotj1uYV0OzG7hX0+huN2E/IdgLDjbiapj1e2fKHrMmGFaIvI6xzzJIQJF9GiRZ7+0j' \
                  'NFLKSyzX/K3JAyFrIPObfwM+y+zAgE1sWcZ1YnuBhICyRHBhaJDKIZL8MywrEfB2yF+R3k9w' \
                  'FG1oN48gSLyfrfEKuB/qgNp+BeTruWUk0AwRE9XVMUuRbjpxa4YA67SKunFEgFGgUfHBeHJT' \
                  'ivvUl0u4Dki1UKAT973P+nXy2O0u239If/kRpNUVhMg8kpk7s8i6Arp7l/705/bLCx4kN5hH' \
                  'HSXIqkiG9tHdeNV8VYo5+72hgaCx3/uVoVLmtvxbOIvo120uTJbuLVTvT8KtsOlb3DxwUrwL' \
                  'zaEMoAQAFk6Q9bNipHxfkRQER4kR7IYTMzSoW5mxh3H9O8Ge5BqVeYMEW36q9wnOYfxOLNw6' \
                  'yQMf8f9sJN4KhZty02xm707S7VEfJJ1KNq7b5pP/3RjE0IKtB2gE6vAPRvRLzEohu0m7q1aU' \
                  'p8wAvSiqjZy7FLaTtLEApXYvLvz6PEJdj4TegCZugj7c8bIOEqLXmloZ6EgVnjQ7/ttys7VF' \
                  'ITB3mazzFiyQuKf4J6+b/a/Y'

    soPath = "/home/lynxi/lockDemo/LDK_Runtime_API_Python_Sample/lib/x86_64/libhasp_linux_x86_64_demo.so"

    ldkHelper = LDKHelper(sVendorCode, soPath)
    try:
        ldkHelper.login()
        data = ldkHelper.encrypt_data("I am caok")
        print("data = ", data)
        data = ldkHelper.decrypt_data()

        ldkHelper.logout()
    except MyError as e:
        print('My exception occurred', e.msg, e.code)

    key = '0CoJUm6Qyw8W8jud'
    data = 'Fh2OSfWBO7y87z98c4BF9A=='

    return key, data
