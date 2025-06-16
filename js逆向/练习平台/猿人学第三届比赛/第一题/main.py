import base64
import time

import requests
import execjs

import random
import string
from PIL import Image
from utils import captha


def generate_custom_id(length=16, suffix='0000'):
    """随机"""
    chars = string.ascii_lowercase + string.digits
    random_length = length - len(suffix)
    prefix = ''.join(random.choices(chars, k=random_length))
    return prefix + suffix


def get_a():
    """获取a值"""
    randon_id = generate_custom_id()
    print("randon_id:::", randon_id)
    t = str(int(time.time() * 1000))
    text = randon_id + '咦~，可带劲~。' + t + '俺不中嘞~'
    print('text:::', text)
    res_a = execjs.compile(open('D:\projects\Spider-WebUnlocker\js逆向\练习平台\猿人学第三届比赛\第一题\loader.js',
                                encoding='utf-8').read()).call('get_a', text)
    print('res_a:::', res_a)
    return res_a


def get_resp():
    """獲取結果請求"""
    cookies = {
        'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3': '1748933333',
        'sessionid': 'b45r1lc8kjx35x1amnmc0305y12zw9m2',
        'Hm_lvt_3e4ffd7a3b6387fe4632831f1230b518': '1749091217,1749208870',
        'HMACCOUNT': 'A44C97F7F2332C8E',
        'Hm_lpvt_3e4ffd7a3b6387fe4632831f1230b518': '1749212550',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://match2025.yuanrenxue.cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://match2025.yuanrenxue.cn/match2025/topic/1',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1748933333; sessionid=b45r1lc8kjx35x1amnmc0305y12zw9m2; Hm_lvt_3e4ffd7a3b6387fe4632831f1230b518=1749091217,1749208870; HMACCOUNT=A44C97F7F2332C8E; Hm_lpvt_3e4ffd7a3b6387fe4632831f1230b518=1749212550',
    }

    a = get_a()

    data = {
        'a': a,
    }

    response = requests.post(
        'https://match2025.yuanrenxue.cn/match2025/topic/1_captcha_jpg',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    data = response.json()
    print(data)
    return data['result']


def save_img(img_b64):
    print(img_b64)
    # 解码Base64
    image_data = base64.b64decode(img_b64)

    # 保存为图片文件
    with open(r"D:\projects\Spider-WebUnlocker\js逆向\练习平台\猿人学第三届比赛\第一题\cap.gif",
              "wb") as f:  # 可改为 .png .webp 等根据需要
        f.write(image_data)

    print("图片已保存为 cap.gif")


def main():
    res_b64 = get_resp()
    # 识别验证码
    res = captha(res_b64)
    print('最终结果：' , res)


if __name__ == '__main__':
    main()
