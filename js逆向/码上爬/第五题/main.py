import json
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from CoreUtils.ua import get_random_ua
from CoreUtils.proxy import get_proxy
from CoreUtils.Encrypt import md5_encrypt, words_to_bytes


def aes_encrypt(plaintext: str, key: bytes, iv: bytes) -> str:
    """
    AES CBC 模式加密，返回 Hex 编码的密文
    :param plaintext: 明文
    :param key: 16/24/32 字节密钥
    :param iv: 16 字节初始化向量
    :return: Hex 编码的密文
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plaintext.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded_text)

    # Convert the encrypted bytes to hex
    hex_encrypted = encrypted.hex()  # Use `hex()` to convert to hex format
    return hex_encrypted


res = []
for i in range(1, 21):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))
    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1745931531,1746426452',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': tt,
    }

    headers = {
        'Host': 'www.mashangpa.com',
        # 'Cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1745931531,1746426452; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746428109',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': ua,
        'sec-ch-ua-mobile': '?0',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.mashangpa.com/problem-detail/3/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'priority': 'u=1, i',
    }

    params = {
        'page': str(i),
        '_ts': tt,
    }

    key = {
        "words": [
            1785673834,
            964118391,
            624314466,
            2019968622
        ],
        "sigBytes": 16
    }
    iv = {
        "words": [
            808530483,
            875902519,
            943276354,
            1128547654
        ],
        "sigBytes": 16
    }
    key = words_to_bytes(key["words"], key["sigBytes"])
    iv = words_to_bytes(iv["words"], iv["sigBytes"])

    aes = aes_encrypt(json.dumps(params) , key, iv)

    print(aes)

    json_data = {
        'xl': aes,
    }

    response = requests.post('https://www.mashangpa.com/api/problem-detail/5/data/', cookies=cookies, headers=headers,
                             json=json_data)

    data = response.json()
    print(data)
    nums = data['current_array']
    print(nums)
    res.extend(nums)
    # time.sleep(1)
print(sum(res))
