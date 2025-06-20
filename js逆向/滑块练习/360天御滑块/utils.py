from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import hashlib


def md5_hash(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()


def encrypt_long(plaintext: str, pem_key: str) -> str:
    rsa_key = RSA.import_key(pem_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    max_len = rsa_key.size_in_bytes() - 11

    encrypted = []
    for i in range(0, len(plaintext), max_len):
        chunk = plaintext[i:i + max_len]
        enc = cipher.encrypt(chunk.encode())
        encrypted.append(base64.b64encode(enc).decode())
    return ''.join(encrypted)


def format_pem(pem_raw: str) -> str:
    # 去除前后空白字符
    pem_raw = pem_raw.strip()

    # 若已有标头，先移除再格式化
    pem_body = pem_raw.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").strip()

    # 每64字符换一行（PEM标准）
    lines = [pem_body[i:i+64] for i in range(0, len(pem_body), 64)]
    formatted = "-----BEGIN PUBLIC KEY-----\n" + "\n".join(lines) + "\n-----END PUBLIC KEY-----"

    return formatted


def encrypt(data: str, token: str, captcha_id: str, k_b64: str) -> str:
    k_decoded = base64.b64decode(k_b64).decode()
    pem_key = format_pem(k_decoded)  # 修复格式
    encrypted_data = encrypt_long(data, pem_key)
    checksum = md5_hash(captcha_id + token)
    return encrypted_data + checksum

