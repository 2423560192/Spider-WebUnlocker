import random
import subprocess
import time
import uuid

import requests
import json
import ddddocr
import execjs


def get_uuid():
    return str(uuid.uuid4())


def get_base_data(uuid):
    """
    获取基础的一些滑块信息
    :return:
    """
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://fcbox.com",
        "Pragma": "no-cache",
        "Referer": "https://fcbox.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = f"https://acs.fcbox.com/captcha/querySlideImage/{uuid}"
    data = {}
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)

    print(response.json())
    print(response)
    data = response.json()

    # 处理数据
    checkId = data["data"]["checkId"]
    clientIp = data["data"]["clientIp"]
    key = data["data"]["key"]
    shadeImageUrl = data["data"]["shadeImageUrl"]
    slideImageUrl = data["data"]["slideImageUrl"]

    return checkId, clientIp, key, shadeImageUrl, slideImageUrl


def parse_slide(bg_url, fg_url):
    """
    生成距离
    :param bg_url:
    :param fg_url:
    :return:
    """
    # bg_url = 'https://consumerapp-1251779293.file.myqcloud.com/captcha/slide/online/20255/b3061e501d114712a9d0367dafe0a509.png'
    # fg_url = 'https://consumerapp-1251779293.file.myqcloud.com/captcha/slide/online/20255/ee61273abcdf4900937a05ad979a6610.png'
    with open('./x1-bg.jpg', 'wb') as f:
        f.write(requests.get(bg_url).content)
    with open('./x2-fg.jpg', 'wb') as f:
        f.write(requests.get(fg_url).content)
    with open('./x1-bg.jpg', 'rb') as f:
        bg_bytes = f.read()
    with open('./x2-fg.jpg', 'rb') as f:
        front_bytes = f.read()
    ocr = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    result = ocr.slide_match(target_bytes=front_bytes,
                             background_bytes=bg_bytes, simple_target=True)

    slide_distance = result['target'][0]
    return int(slide_distance), result['target'][1]


def parse_traceData(slide_distance, pointY):
    traceData = []
    x = 0
    y = pointY
    t = int(time.time() * 1000)
    while x < slide_distance:
        trace = {"x": x, "y": y, "time": t}
        traceData.append(trace)
        x += random.randint(0, 5)
        y = pointY
        t += random.randint(1, 20)
        if x >= slide_distance:
            x = slide_distance
            trace = {"x": x, "y": y, "time": t}
            traceData.append(trace)
            break
    # for i in range(5):
    #     trace = {"x": x, "y": y, "time": t}
    #     traceData.append(trace)
    #     x = slide_distance
    #     y = pointY
    #     t += random.randint(1, 20)
    return json.dumps(traceData)


def get_token(enc, uuid):
    """
    获取token
    :param enc:
    :return:
    """
    import requests

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://fcbox.com",
        "Pragma": "no-cache",
        "Referer": "https://fcbox.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = f"https://acs.fcbox.com/captcha/checkCode/{uuid}"
    data = enc.encode(
        'unicode_escape')
    print(data)
    response = requests.post(url, headers=headers, data=data)

    print(response.text)
    print(response)


def get_data(checkId, clientIp, key, shadeImageUrl, slideImageUrl, uuid):
    # 距离
    slide, pointY = parse_slide(shadeImageUrl, slideImageUrl)
    print(slide)
    # 轨迹
    track = parse_traceData(slide, pointY)
    print(track)

    # 生成加密值
    result = subprocess.run(
        ["node", "loader.js", checkId, clientIp, key, uuid, track],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


if __name__ == '__main__':
    uuid = get_uuid()
    print(uuid)
    # 获取滑块信息
    checkId, clientIp, key, shadeImageUrl, slideImageUrl = get_base_data(uuid)
    print(checkId, clientIp, key, shadeImageUrl, slideImageUrl)

    enc = get_data(checkId, clientIp, key, shadeImageUrl, slideImageUrl, uuid)

    get_token(enc, uuid)
