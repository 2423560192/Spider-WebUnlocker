import requests

pwd = '123456'

data = {
    'phone': '17782200195',
    'password': pwd,
}

import hashlib


def md5_sign(sb):
    token = ''
    reqTime = '1744179117915'
    noncestr = '123456'[2:]
    str = sb

    encrypt = token + reqTime + noncestr + str
    md5 = hashlib.md5()
    md5.update(encrypt.encode('utf-8'))
    print(md5.hexdigest())
    return md5.hexdigest()


md5 = hashlib.md5()
md5.update(pwd.encode('utf-8'))
pwd = md5.hexdigest()
data['password'] = pwd
print(pwd)

sb = "&".join([f"{k}={v}" for k, v in data.items()])
sign = md5_sign(sb)

print('sign:', sign)

headers = {
    'X-App': 'native',
    'X-Noncestr': '123456',
    'X-OS': 'partnerApp_android',
    'X-Req-Time': '1744179117915',
    'X-Sign': sign,
    'Host': 'chinayltx.com',
    'User-Agent': 'okhttp/3.10.0',
    'Content-Type': 'application/x-www-form-urlencoded',
}
response = requests.post('https://chinayltx.com/app/api/v1/partnerLogin/login', headers=headers, data=data)
print(response.json())
