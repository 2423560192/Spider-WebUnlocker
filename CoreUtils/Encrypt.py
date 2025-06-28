import hashlib

from Crypto.Cipher import AES, DES3
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


import hmac
import hashlib
import base64


def generate_hmac_sha1(message: str, secret: str, output_format: str = 'hex') -> str:
    """
    生成 HMAC-SHA1 签名。

    参数:
        message (str): 要签名的消息。
        secret (str): 用于签名的密钥。
        output_format (str): 输出格式，可选 'hex' 或 'base64'（默认 'hex'）。

    返回:
        str: 签名结果（十六进制或 Base64 编码）。
    """
    message_bytes = message.encode('utf-8')
    secret_bytes = secret.encode('utf-8')
    signature = hmac.new(secret_bytes, message_bytes, hashlib.sha1)

    if output_format == 'base64':
        return base64.b64encode(signature.digest()).decode()
    else:
        return signature.hexdigest()


class Des3:
    """3DES 加密解密"""
    def __init__(self, key: str, iv: str):
        # 取前24字节做key，确保符合3DES要求
        raw_key = key.encode("utf-8")[:24]
        self.key = DES3.adjust_key_parity(raw_key)  # 调整奇偶校验位

        # IV必须是8字节
        self.iv = iv.encode("utf-8")[:8]

    def encrypt(self, data: str) -> str:
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv=self.iv)
        padded_data = pad(data.encode("utf-8"), DES3.block_size)
        encrypted = cipher.encrypt(padded_data)
        # 返回base64字符串，方便存储/传输
        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, b64data: str) -> str:
        encrypted = base64.b64decode(b64data)
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv=self.iv)
        decrypted = cipher.decrypt(encrypted)
        unpadded = unpad(decrypted, DES3.block_size)
        return unpadded.decode("utf-8")
