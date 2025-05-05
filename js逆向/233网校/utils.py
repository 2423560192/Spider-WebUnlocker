import hashlib
import json
import urllib.parse
import time

import random
from datetime import datetime

from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import base64


def generate_c():
    now = datetime.now()

    # 格式化时间
    timestamp = "{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    )

    # 生成两个 5 位数的随机整数
    rand1 = random.randint(10000, 99999)
    rand2 = random.randint(10000, 99999)

    return f"ucpage{timestamp}{rand1}{rand2}"


def generate_signature(method, c, params, is_form_data=False):
    salt = "RZRRNN9RXYCP"

    if is_form_data:
        raw = salt + c
    elif method.lower() == "get":
        raw = salt + c + urllib.parse.unquote(params)
    else:
        params_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
        raw = salt + c + params_str

    md5_hash = hashlib.md5(raw.encode('utf-8')).hexdigest().upper()
    return md5_hash


def decrypt_content(e):
    """
    解密内容
    """
    if not isinstance(e, str):
        return e

    try:
        key = b"ea9377ea"  # 密钥
        iv = bytes([0] * 8)  # IV

        cipher = DES.new(key, DES.MODE_CBC, iv)
        decrypted = cipher.decrypt(base64.b64decode(e))
        return unpad(decrypted, DES.block_size).decode('utf-8')
    except Exception as ex:
        print("解密失败:", ex)
        return e


def save_to_json(questions, filename="questions.json"):
    """
    将题目信息保存到JSON文件
    """
    with open(filename, 'a+', encoding='utf-8') as f:
        # 保存为JSON格式，确保中文不被转义
        json.dump(questions, f, ensure_ascii=False, indent=2)


def get_sid_sign(method, data, is_form_data=False):
    """
    加密参数
    """
    method = method
    # sid
    sid = generate_c()
    # sign
    signature = generate_signature(method, sid, data, is_form_data)

    return sid, signature
