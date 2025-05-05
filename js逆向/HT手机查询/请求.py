import json
import base64
import random
import time

import requests
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import get_random_bytes


# =================== AES 加密 & 解密 ===================
def encryptAES(data: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    padded = pad(data.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(encrypted).decode('utf-8')


def decryptAES(data: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    encrypted_data = base64.b64decode(data)
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted.decode('utf-8')


# =================== RSA 加密 ===================
def encryptRSA(data: str, public_key_str: str) -> str:
    pub_key = RSA.import_key("""-----BEGIN PUBLIC KEY-----\n""" + public_key_str + """\n-----END PUBLIC KEY-----""")
    cipher = PKCS1_v1_5.new(pub_key)
    encrypted = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')


# =================== 时间处理 ===================
def getReqTime():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


# =================== 主请求函数 ===================
def axiosHTTP(data: dict, serviceId: str):
    rsa = ('MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs4VXnzCnGoOr0camO/'
           'kB/KC+cM57FoIHnAVyvUOLgLWTptP76hC/FD/yBjdVHMzcBazkJuTVKvhd5Y+31YNS'
           'R3wPjMwus9re7AQdj8DI5RnZdRjXtLfKxG/PC8MlJ98rkZYXg6vp1xyo3Oq9qXJ1ff9'
           'WJOAMSAS6dfkzA+qSumw1UzpX1duhAm8QhYAbEW24Leto55uuoUKnS5LXAN8qVe5uKL'
           'ueb787xQm5NTj2M3eB0w//NTiKlV3g2JsGJv8H0vShQK0ez5bR73dxyrO0qY6Xr2ri6'
           'Dp2SHNEjdclohoANkNB649tUgadGId546Fvs0Ln0VzW909LCz4vxMKmsQIDAQAB')
    aesKey = '38ef2c46b95bb5237b0312b3'

    reqTime = getReqTime()
    req = {
        "publicData": {
            "reqTime": reqTime,
            "reqSeq": reqTime + "htSearch",
            "activityId": "htSearch",
            "appid": "cxcc7a4a1608df4431",
            "serviceId": serviceId,
            "version": "1.0"
        },
        "data": data
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://gd.10086.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://gd.10086.cn/apph5/htSearch/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'BIGipServerng3dmz_web_2002968450=!69VbXqfQ50psUfbc1tPSJDiawToJFkDCoY2yuPckyxsvT/pp75dNaz5AHVHO6k6wwlcsTeXjgBEAy7w=; JSESSIONID=64F6CB484222769260AC752274C07E7C; zA7uZWGUB1=dy97636rzDr5szYyLMlbOT4StT/NXEGo+BMjJg==; WT_FPC=id=2c548037263aa9511321744808813042:lv=1744808850363:ss=1744808813042',
    }

    encrypted_data = encryptAES(json.dumps(req, separators=(',', ':')), aesKey)
    encrypted_key = encryptRSA(aesKey, rsa)

    url = 'https://gd.10086.cn/apph5/openapi/app/handle2'
    payload = {
        "data": encrypted_data,
        "key": encrypted_key
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        res_json = response.json()

        if res_json.get("data"):
            decrypted = decryptAES(res_json["data"], aesKey)
            res_json["data"] = json.loads(decrypted)

        return res_json

    except requests.RequestException as e:
        print("HTTP error:", e)
        return None
    except Exception as e:
        print("Decrypt or parse error:", e)
        return None


def generate_phone_numbers(n=10):
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '170', '171', '172', '173', '175', '176', '177', '178', '179',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
                '198', '199']
    numbers = []
    for _ in range(n):
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choices('0123456789', k=8))
        numbers.append(prefix + suffix)
    return numbers


# =================== 示例调用 ===================
if __name__ == '__main__':
    phones = generate_phone_numbers()
    phones.append('13802999981')
    for i in phones:
        res = axiosHTTP({
            "servicecode": "Fe90322c88553590",
            "params": {
                "mobile": str(i)
            }
        }, 'ability_customize')

        if res:
            public_data = res.get("publicData", {})
            ret_info = public_data.get("retInfo", {})
            data_result = res.get("data", {}).get("result", {})

            if ret_info.get("retCode") == 0 and data_result.get("status") == 0:
                frontline = data_result.get("data", {}).get("frontline")
                if frontline == -1:
                    print(f"{i}: 否")
                elif frontline == 0:
                    print(f"{i}: 符合HT,不符合充送")
                elif frontline == 1:
                    print(f"{i}: 不符合HT，符合充送")
                elif frontline == 2:
                    print(f"{i}: 符合HT，符合充送")
            else:
                print("请求失败:", ret_info.get("retMsg"))
        else:
            print("请求失败，网络或解析错误")
        time.sleep(2)
