import json
import os
import random
import time
from urllib.parse import urlparse

import ddddocr
import execjs
import requests
from PIL import Image

from CoreUtils.Encrypt import md5_encrypt
from utils import encrypt


def get_sign(tt):
    """
    获取sign
    :return:
    """
    data = {
        "appId": "dc1db94ea7b3843c",
        "dc": 0,
        "ec": 0,
        "hc": 0,
        "nonce": 1748224283042,
        "os": 3,
        "pc": 0,
        "phone": 10000000000,
        "pn": "com.web.tianyu",
        "rc": 0,
        "sdkName": "360CaptchaSDK",
        "timestamp": tt,
        "type": 1,
        "ui": 'null',
        "version": "2.0.0",
        "xc": 0
    }
    s = ''
    for k, v in data.items():
        s += str(k)
        s += str(v)
    return md5_encrypt(s)


def parse_traceData(slide_distance):
    """生成轨迹"""
    traceData = {}
    x = 0
    t = int(time.time() * 1000)
    y = random.randint(210, 220)
    traceData[str(x)] = {'t': t, 'y': y}
    while x < slide_distance:
        x += random.randint(1, 5)
        t += random.randint(10, 20)
        if x >= slide_distance:
            x = slide_distance
            traceData[str(x)] = {'t': t, 'y': y + random.randint(-1, 1)}
            break
        traceData[str(x)] = {'t': t, 'y': y + random.randint(-1, 1)}
    return [traceData]


def get_auth_resp(tt, sign):
    import requests

    headers = {
        "accept": "*/*",
        "accept-language": "zh-cn",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://jiagu.360.cn",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://jiagu.360.cn/",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    url = "https://captcha.jiagu.360.cn/api/v3/auth"
    data = {
        "appId": "dc1db94ea7b3843c",
        "type": "1",
        "version": "2.0.0",
        "pn": "com.web.tianyu",
        "os": "3",
        "sdkName": "360CaptchaSDK",
        "timestamp": tt,
        "nonce": "1748224283042",
        "ui": "null",
        "rc": "0",
        "pc": "0",
        "ec": "0",
        "hc": "0",
        "xc": "0",
        "dc": "0",
        "phone": "10000000000",
        "sign": sign
    }

    # proxies = {
    #     "http": "http://localhost:8888",
    #     "https": "http://localhost:8888",
    # }

    response = requests.post(url, headers=headers, data=data)

    data = response.json()

    k = data['data']['k']
    captchaId = data['data']['captchaId']
    token = data['data']['token']
    front = data['data']['front'][0]
    bg = data['data']['bg'][0]
    print(k, captchaId, token, front, bg)
    return k, captchaId, token, front, bg


def check(track, captchaId, token, distance, k):
    """校验"""
    headers = {
        "accept": "*/*",
        "accept-language": "zh-cn",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://jiagu.360.cn",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://jiagu.360.cn/",
        "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    url = "https://captcha.jiagu.360.cn/api/v3/check"

    report = get_report(track, token, captchaId, k)

    data = {
        "captchaId": captchaId,
        "token": token,
        "length": distance,
        "version": "2.0.0",
        "width": "300",
        "report": report,
        "tracking": "[object Object]"
    }
    response = requests.post(url, headers=headers, data=data)

    print(response.json())


def get_filename_without_extension(url):
    """获取url的文件名"""
    path = urlparse(url).path  # 解析路径部分
    filename = os.path.basename(path)  # 获取最后一个文件名
    name, _ = os.path.splitext(filename)  # 去掉扩展名
    return name


def recover_bg(slice_list):
    """还原数组"""
    bg_img = Image.open('./x1-bg.png')
    recover_img = Image.new('RGBA', (544, 284), 'white')
    for index, item in enumerate(slice_list):
        x = index * 17
        y = 0
        l = bg_img.crop((x, y, x + 17, y + 284))
        recover_img.paste(l, (item * 17, 0))
    recover_img.save('./x2-recover-bg.png')
    return


def restore_img(front, bg):
    """还原并保存图片"""
    # 保存图片
    with open(r'./x1-front.png', 'wb') as f:
        f.write(requests.get(front).content)
    with open(r'./x1-bg.png', 'wb') as f:
        f.write(requests.get(bg).content)
    last_name = get_filename_without_extension(front)
    print('last_name： ', last_name)
    # 获取iv数组
    iv = execjs.compile(open(r'D:\projects\Spider-WebUnlocker\js逆向\滑块练习\360天御滑块\loader.js', 'r',
                             encoding='utf-8').read()).call("shuzu_list", last_name)
    print('iv:::', iv)
    # 还原数组
    recover_bg(iv)


def get_slide_distance():
    """获取滑动距离"""
    with open('./x2-recover-bg.png', 'rb') as f:
        bg_bytes = f.read()
    with open('./x1-front.png', 'rb') as f:
        front_bytes = f.read()
    ocr = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    result = ocr.slide_match(target_bytes=front_bytes,
                             background_bytes=bg_bytes, simple_target=True)

    return int(result['target'][0] * 300 / 544)


def get_report(slide_list, token, captcha_id, k):
    data = json.dumps(slide_list)
    print('data：', data)
    result = encrypt(data, token, captcha_id, k)
    print('加密结果：', result)
    return result


def main():
    tt = str(int(time.time() * 1000))
    # 第一次请求
    sign = get_sign(tt)
    k, captchaId, token, front, bg = get_auth_resp(tt, sign)
    print('k:::', k)
    print('captchaId:::', captchaId)
    print('token:::', token)

    # 还原并保存图片
    restore_img(front, bg)

    # 获取滑动距离
    distance = get_slide_distance()
    print('距离：', distance)
    # 生成轨迹
    trace_list = parse_traceData(distance)
    print('轨迹：', trace_list)
    # 第二次请求
    check(trace_list, captchaId, token, distance, k)


if __name__ == '__main__':
    main()
