import requests
import time
import hashlib


def get_sign(j: int, channel='android') -> str:
    try:

        # 第一个 MD5: "niaodaifu" + j
        s1 = "niaodaifu" + str(j)
        md5_1 = hashlib.md5(s1.encode()).hexdigest()
        part1 = md5_1[12:30]

        # 第二个 MD5: channel + j
        s2 = channel + str(j)
        md5_2 = hashlib.md5(s2.encode()).hexdigest()
        part2 = md5_2[12:26]

        return part1 + part2
    except Exception as e:
        print("Error:", e)
        return ""


headers = {
    'Host': 'api.niaodaifu.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'devisetoken': '-',
    'password': '5201314',
    'mobile': '17782200193',
    'channel': 'android',
    'sign': get_sign(1744178331),
    'time': '1744178331',
    'mechanism': '0',
    'platform': '1',
}

response = requests.post('https://api.niaodaifu.cn/v4/site/loginnew', headers=headers, data=data)
print(response.json())