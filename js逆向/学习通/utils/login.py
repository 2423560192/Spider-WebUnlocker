import base64

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def encrypt_by_AES(message, key):
    # 解析 UTF-8 编码的密钥和消息
    key_bytes = key.encode('utf-8')
    message_bytes = message.encode('utf-8')

    # 初始化 AES 加密器，使用 CBC 模式和 PKCS7 填充
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=key_bytes)

    # 加密消息
    encrypted_bytes = cipher.encrypt(pad(message_bytes, AES.block_size))

    # 将加密后的字节转换为 Base64 编码字符串
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')

    return encrypted_base64


def auto_login(username, pwd):
    key = "u2oh6Vu^HWe4_AES"

    phone = str(username)
    pwd = str(pwd)
    phone = encrypt_by_AES(phone, key)
    pwd = encrypt_by_AES(pwd, key)

    url = 'https://passport2.chaoxing.com/fanyalogin'
    data = {
        'uname': phone,
        'password': pwd,
        'fid': '-1',
        'refer': 'https://i.chaoxing.com/',
        't': 'true'
    }
    session = requests.session()
    resp = session.post(url, data=data)
    status = resp.json()['status']
    if status:
        return resp.cookies.get_dict()
    else:
        return False

