from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


class AESClass:
    def __init__(self, key, iv):
        self.key = key.encode()   # 秘钥
        self.iv = iv.encode()   # 偏移量

    def encryption(self, text):
        """
        加密
        :param test.txt: 需要加密的内容
        :return:
        """
        text = pad(text.encode(), 16)

        aes = AES.new(self.key, AES.MODE_CBC, self.iv)  # 创建一个aes对象

        en_text = aes.encrypt(text)  # 加密明文

        en_text = base64.b64encode(en_text).decode()  # 将返回的字节型数据转进行base64编码

        return en_text

    def decryption(self, text):
        """
        解密
        :param text: 密文
        :return:
        """

        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        text = text.encode()  # 需要解密的文本
        ecrypted_base64 = base64.b64decode(text)  # base64解码成字节流
        source = aes.decrypt(ecrypted_base64)  # 解密
        return unpad(source, 16).decode()
