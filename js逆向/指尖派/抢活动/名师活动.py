import base64
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

ENCRYPT_KEY = "gNuRigdKZ4rMwKnpL2TXH4v51h33rRqt"


def encrypt(text):
    """
    实现与项目完全一致的AES-ECB加密
    """
    if text is None or len(text) == 0:
        return ""

    # 转换密钥为UTF-8编码的字节
    key_bytes = ENCRYPT_KEY.encode('utf-8')

    # 创建AES-ECB加密器
    cipher = AES.new(key_bytes, AES.MODE_ECB)

    # 加密数据（使用PKCS7填充）
    text_bytes = text.encode('utf-8')
    padded_bytes = pad(text_bytes, AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_bytes)

    # 转换为Base64字符串，与CryptoJS.AES.encrypt输出格式一致
    return base64.b64encode(encrypted_bytes).decode('utf-8')


def get_user_sign(timestamp):
    """
    生成与小程序相同的User-Sign头
    """
    return encrypt(str(timestamp))


timestamp = int(time.time() * 1000)
user_sign = get_user_sign(str(timestamp))
headers = {
    'Host': 'h5.wmzjp.com',
    'accept': 'application/json, text/plain, */*',
    'user-sign': user_sign,
    'xweb_xhr': '1',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdXRoIjp7InBhc3N3b3JkIjpudWxsLCJ1c2VybmFtZSI6InpqcDEwMDEwMDAwNTMxMjciLCJhdXRob3JpdGllcyI6W10sImFjY291bnROb25FeHBpcmVkIjp0cnVlLCJhY2NvdW50Tm9uTG9ja2VkIjp0cnVlLCJjcmVkZW50aWFsc05vbkV4cGlyZWQiOnRydWUsImVuYWJsZWQiOnRydWUsInVzZXJJZCI6MTAwMTAwMDA1MzEyNywib3BlbklkIjoib0ZPODI2U2lSRjlCbE5KVXo3bWxoMWptaE8wYyIsInNjaG9vbElkIjo2LCJiaW5kZWQiOjB9LCJqdGkiOiIwYTk4MDY0NS0yZjc0LTQ4NjUtODY5MC02YmZhZDg1N2ZhNjUiLCJpYXQiOjE3NDU1NjI4MTYsImV4cCI6MTc0NjE2NzYxNn0.6JH4rptGrubuvobBZZedZ2zRGN99YFjZRLXwJBPo9OE',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
    'Content-type': 'application/json;charset=UTF-8',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://servicewechat.com/wxbd5a45d082ccacaa/36/page-frame.html',
    'accept-language': 'zh-CN,zh;q=0.9',
}


json_data = {
    'activityId': '16736',
    'countNumber': 1,
    'femaleNumber': 0,
    'maleNumber': 1,
    'personalNumber': 1,
    'teamNumber': 0,
    'teamTotalNumber': 0,
    'attendNumber': 1,
    'viewNumber': 0,
    'userId': 1001000053127,
    'role': 2,
    'roleName': '参加者',
    'enrollWay': 1,
    'url': '',
    'name': '',
}



response = requests.post('https://h5.wmzjp.com/zjp/act-activity-applicants/confirmEnroll', headers=headers, json=json_data)


print(response.json())