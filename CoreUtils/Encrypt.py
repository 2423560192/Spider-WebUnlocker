import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


def md5_encrypt(text):
    """
    对输入字符串进行 MD5 加密，返回加密后的十六进制字符串。
    """
    if not isinstance(text, str):
        raise TypeError("输入必须是字符串类型")

    md5_obj = hashlib.md5()
    md5_obj.update(text.encode('utf-8'))
    return md5_obj.hexdigest()


class AESCipher:
    """
    AES
    """

    def __init__(self, key: bytes, iv: bytes):
        """
        key: AES 密钥 (16/24/32 字节)
        iv:  初始向量 IV (16 字节)
        """
        if len(key) not in [16, 24, 32]:
            raise ValueError("密钥必须是 16/24/32 字节")
        if len(iv) != 16:
            raise ValueError("IV 必须是 16 字节")

        self.key = key
        self.iv = iv

    def encrypt(self, plaintext: str) -> str:
        """
        加密字符串，返回 Base64 编码密文
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded = pad(plaintext.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded)
        return base64.b64encode(encrypted).hex()

    def decrypt(self, ciphertext_b64: str) -> str:
        """
        解密 Base64 编码密文，返回原文字符串
        """
        ciphertext = base64.b64decode(ciphertext_b64)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode('utf-8')


def words_to_bytes(words, sig_bytes):
    """
    将 CryptoJS 格式的 words 数组转为 Python bytes
    """
    b = bytearray()
    for word in words:
        b.extend(word.to_bytes(4, byteorder='big'))  # CryptoJS 使用大端序
    return bytes(b[:sig_bytes])  # 截取 sigBytes 长度


def sha256(data):
    hash_object = hashlib.sha256(data.encode())
    sha256_hash = hash_object.hexdigest()
    return sha256_hash
