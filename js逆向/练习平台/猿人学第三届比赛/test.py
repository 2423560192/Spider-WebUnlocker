from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64


def so(plaintext, key, iv):
    # 补全密钥和IV到16字节（32个字符）
    key = key.ljust(32, '0')[:32]  # 确保密钥长度为32个字符
    iv = iv.ljust(32, '0')[:32]  # 确保IV长度为32个字符

    # 转换为字节
    key_bytes = bytes.fromhex(key)
    iv_bytes = bytes.fromhex(iv)

    # 创建AES加密器（CBC模式）
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

    # 填充明文到16字节的倍数
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)

    # 加密并编码为Base64
    ciphertext = cipher.encrypt(padded_plaintext)
    return base64.b64encode(ciphertext).decode('utf-8')


# 测试
result = so("123456", "0000000000000000", "0000000000000000")
print(f"加密结果: {result}")  # 输出应为 D4Vvd68nVYJiD0ihJ1nr/w==