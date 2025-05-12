import hashlib

import time

data = {
    'nonce': 'OhaxW9oes6',  # 这里需要填充实际的 nonce 值
    'ts': str(int(time.time() * 1000))  # 这里需要填充实际的 ts 值
}

# 模拟从输入框获取用户密码的操作
user_password = '5201314'  # 这里填充实际的用户密码

# 第一次 SHA-1 哈希操作
pwd = hashlib.sha1(user_password.encode('utf-8')).hexdigest()

# 第二次 SHA-1 哈希操作，nonce + ts + pwd
combined_string = data['nonce'] + data['ts'] + pwd
final_pwd = hashlib.sha1(combined_string.encode('utf-8')).hexdigest()

print(final_pwd)

import requests

cookies = {
    'acw_tc': 'ddb2069a17382216691367223e89815e6a5cf2fa3f1937db2fa85efa90',
    'cdn_sec_tc': 'ddb2069a17382216691367223e89815e6a5cf2fa3f1937db2fa85efa90',
    'PHPSESSID': 'jg8novr9fhq468kg3vqmlfpn84',
    'doyo_www_uv_mark': 'true',
    'Hm_lvt_b0affa74a0ef00f793803b2ae8a25f8a': '1738221671',
    'HMACCOUNT': '74E03469813A9187',
    'Hm_lpvt_b0affa74a0ef00f793803b2ae8a25f8a': '1738222254',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'acw_tc=ddb2069a17382216691367223e89815e6a5cf2fa3f1937db2fa85efa90; cdn_sec_tc=ddb2069a17382216691367223e89815e6a5cf2fa3f1937db2fa85efa90; PHPSESSID=jg8novr9fhq468kg3vqmlfpn84; doyo_www_uv_mark=true; Hm_lvt_b0affa74a0ef00f793803b2ae8a25f8a=1738221671; HMACCOUNT=74E03469813A9187; Hm_lpvt_b0affa74a0ef00f793803b2ae8a25f8a=1738222254',
    'Origin': 'https://www.doyo.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.doyo.cn/passport/login?next=https://www.doyo.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'username': 'Jkingkd',
    'password': final_pwd,
    'remberme': '1',
    'next': 'aHR0cHMlM0ElMkYlMkZ3d3cuZG95by5jbiUyRg==',
}

response = requests.post('https://www.doyo.cn/User/Passport/login', cookies=cookies, headers=headers, data=data)

print(response.text)
