import base64
import hashlib
import time
import uuid

import requests
from Crypto.Cipher import DES3

from CoreUtils.Encrypt import md5_encrypt, Des3


def get_sign(sign_type: int, param_map: dict) -> str:
    # 获取sign
    KEY_V2 = "W@oC!AH_6Ew1f6%8"
    # 选择 key
    if sign_type == 1:
        key = KEY_V2

    # 构造字符串：key + param1name + param1value + ... + key
    sb = [key]
    for k in sorted(param_map.keys()):  # TreeMap 相当于 key 排序后的 dict
        sb.append(k)
        sb.append(str(param_map[k]))
    sb.append(key)

    sign_str = ''.join(sb)
    print('sign_str', sign_str)
    md5 = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    print('sign', md5)
    return md5


def get_pwd(s):
    """加密密码"""
    print('pwd', md5_encrypt(s))
    return md5_encrypt(s)


# encode3Des 算法
def des3(data_string):
    BS = 8
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    # 3DES的MODE_CBC模式下只有前24位有意义
    key = b'appapiche168comappapiche168comap'[0:24]
    iv = b'appapich'

    plaintext = pad(data_string).encode("utf-8")

    # 使用MODE_CBC创建cipher
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    result = cipher.encrypt(plaintext)
    return base64.b64encode(result).decode('utf-8')


def get_udid():
    """获取udid"""
    timestamp = str(int(time.time()))
    des_3 = Des3(iv="appapich", key="appapiche168comappapiche168comap"[:24])
    p = str(uuid.uuid4()) + "|" + timestamp + ".000000|" + "453999"

    print('p', p)
    udid = des_3.encrypt(p)
    print('udid', udid)
    return udid


headers = {
    'Host': 'dealercloudapi.che168.com',
    'cache-control': 'public, max-age=0',
    'traceid': 'atc.android_fbfc9427-7ceb-492f-b896-556248b7d390',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'okhttp/3.14.9',
}

username = '17782200192'
pwd = '123456'

pwd = get_pwd(pwd)

udid = get_udid()

dic = {
  "_appid": "atc.android",
  "appversion": "3.78.0",
  "channelid": "csy",
  "pwd": pwd,
  "signkey": "",
  "type": "",
  "udid": udid,
  "username": username
}

_sign = get_sign(1, dic)

data = {
    '_appid': 'atc.android',
    '_sign': _sign,
    'appversion': '3.78.0',
    'channelid': 'csy',
    'pwd': pwd,
    'signkey': '',
    'type': '',
    'udid': udid,
    'username': username,
}

response = requests.post('https://dealercloudapi.che168.com/tradercloud/sealed/login/login.ashx', headers=headers,
                         data=data)

print(response.text)
