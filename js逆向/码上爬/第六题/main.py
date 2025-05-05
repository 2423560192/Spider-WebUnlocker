import binascii
import json
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from CoreUtils.ua import get_random_ua

import urllib.parse
from CoreUtils.Encrypt import md5_encrypt


def get_s(tt):
    return md5_encrypt("sssssbbbbb" + tt)


def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))
    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1745931531,1746426452',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': tt,
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mashangpa.com/problem-detail/6/',
        's': get_s(tt),
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'tt': tt,
        'user-agent': ua,
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1745931531,1746426452; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746429714',
    }

    params = {
        'page': page,
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/6/data/', params=params, cookies=cookies,
                            headers=headers)

    data = response.json()
    print(data)
    return data


def xxxooo(encryptedHex):
    # 将字符串转换为字节数组
    kkkk = b"xxxxxxxxoooooooo"  # 密钥，字符串直接转为字节
    iiii = b"0123456789ABCDEF"  # 初始化向量，字符串直接转为字节

    # 将加密的十六进制字符串转换为字节数据
    encrypted_bytes = binascii.unhexlify(encryptedHex)

    # 使用传入的密钥和初始化向量创建 AES CBC 模式解密器
    cipher = AES.new(kkkk, AES.MODE_CBC, iiii)

    # 解密数据并去除填充
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

    # 将解密后的字节数据转换为 UTF-8 字符串
    return decrypted_bytes.decode('utf-8')


def parse_data(data):
    nums = data['t']
    res_data = xxxooo(nums)

    nums = json.loads(res_data)['current_array']
    print(nums)

    return nums


if __name__ == '__main__':
    res_sum = []
    for i in range(1, 21):
        resp = get_resp(str(i))
        nums = parse_data(resp)
        res_sum.extend(nums)
    print(sum(res_sum))
