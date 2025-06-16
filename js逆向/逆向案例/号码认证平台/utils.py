from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class AESCipherCBC:
    def __init__(self, key: str, iv: str):
        self.key = key.encode('utf-8')    # 必须是 16/24/32 字节
        self.iv = iv.encode('utf-8')      # 必须是 16 字节

    def encrypt(self, data: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return base64.b64encode(ct_bytes).decode('utf-8')

    def decrypt(self, enc: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ct = base64.b64decode(enc)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')