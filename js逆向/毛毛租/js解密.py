# """
# url: https://www.maomaozu.com/#/build
# """
import json
import subprocess

from functools import partial

import requests

subprocess.Popen = partial(subprocess.Popen, encoding="UTF-8")

from js逆向.utils.AesJ import AESClass

cookies = {
    'SECKEY_ABVK': 'XrKu5LLdlblG51Mz4A0nxcR0yI8euCGVKlFchR0an37GNtlZOV7Z2Qj1kjGceIxWsTZi/Goh4rbGQS+IyIgbgw%3D%3D',
    'BMAP_SECKEY': 'XrKu5LLdlblG51Mz4A0nxcR0yI8euCGVKlFchR0an34ckrzq8C_eY5PUO-AllHkKEbgeigCwTW6N2MY1dcd4RL_LzinXwkOwyZLHU-SzYETivrgRKcs6HUdGCXlv6LjpmRToTXQbyg6JWvQD27ggKDvLWu_xaF3vnWP5RwJsiTqjoWOcCT4Sou9cGqEXmszPfqW5kx_6RdHFwo3UxHidEw',
    'PHPSESSID': '6h5j21qau21rmbbm5c3j2h5e26',
    'Hm_lvt_6cd598ca665714ffcd8aca3aafc5e0dc': '1729169071',
    'HMACCOUNT': '74E03469813A9187',
    'Hm_lpvt_6cd598ca665714ffcd8aca3aafc5e0dc': '1729169470',
    'SECKEY_ABVK': 'XrKu5LLdlblG51Mz4A0nxcR0yI8euCGVKlFchR0an35hUm/aflB4IrEHlSqOLav3JcMeHzyeQJosMp5CP/oOdQ%3D%3D',
    'BMAP_SECKEY': 'XrKu5LLdlblG51Mz4A0nxcR0yI8euCGVKlFchR0an34ckrzq8C_eY5PUO-AllHkKD7SVz8JXZwvKc5MOMbDn301nE3RhuL_KIWnc2FPK80o021_2VP8CzcESj4v7VvnHOJLr1scBxGpcCfMQ_YGzMuJx150BFafkXqSxcnveAtMbS1VlEnM4i28BDi77Nvf5bLAjyo0ZpvjvAoKwdWOkYg',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    # 'Cookie': 'SECKEY_ABVK=XrKu5LLdlblG51Mz4A0nxcR0yI8euCGVKlFchR0an37GNtlZOV7Z2Qj1kjGceIxWsTZi/Goh4rbGQS+IyIgbgw%3D%3D; BMAP_SECKEY=XrKu5LLdlblG51Mz4A0nxcR0yI8euCGVKlFchR0an34ckrzq8C_eY5PUO-AllHkKEbgeigCwTW6N2MY1dcd4RL_LzinXwkOwyZLHU-SzYETivrgRKcs6HUdGCXlv6LjpmRToTXQbyg6JWvQD27ggKDvLWu_xaF3vnWP5RwJsiTqjoWOcCT4Sou9cGqEXmszPfqW5kx_6RdHFwo3UxHidEw; PHPSESSID=6h5j21qau21rmbbm5c3j2h5e26; Hm_lvt_6cd598ca665714ffcd8aca3aafc5e0dc=1729169071; HMACCOUNT=74E03469813A9187; Hm_lpvt_6cd598ca665714ffcd8aca3aafc5e0dc=1729169470; SECKEY_ABVK=XrKu5LLdlblG51Mz4A0nxcR0yI8euCGVKlFchR0an35hUm/aflB4IrEHlSqOLav3JcMeHzyeQJosMp5CP/oOdQ%3D%3D; BMAP_SECKEY=XrKu5LLdlblG51Mz4A0nxcR0yI8euCGVKlFchR0an34ckrzq8C_eY5PUO-AllHkKD7SVz8JXZwvKc5MOMbDn301nE3RhuL_KIWnc2FPK80o021_2VP8CzcESj4v7VvnHOJLr1scBxGpcCfMQ_YGzMuJx150BFafkXqSxcnveAtMbS1VlEnM4i28BDi77Nvf5bLAjyo0ZpvjvAoKwdWOkYg',
    'Origin': 'https://www.maomaozu.com',
    'Referer': 'https://www.maomaozu.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# data = 'i1gpLEJyKvluv3sQVGr/hxLFjGY10ceRduSzH2ioPFBjfi8rrpaAvyzrSKwP5PDU'

# data = "{\"Type\":0,\"page\":5,\"expire\":1729170335046}"

data = json.dumps({"Type": 0, "page": 5, "expire": 1729170335046})

key = '55b3b62613aef1a0'
iv = '55b3b62613aef1a0'

aes = AESClass(key, iv)
data = aes.encryption(data)
print(data)

response = requests.post('https://www.maomaozu.com/index/build.json', cookies=cookies, headers=headers, data=data)

print(response.text)

res = response.text

# 解密

aes_dec = AESClass(key='0a1fea31626b3b55', iv='0a1fea31626b3b55')

print(aes_dec.decryption(res))
