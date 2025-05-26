import time

from CoreUtils.Encrypt import md5_encrypt


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
    print(s)
    print(md5_encrypt(s))
    return md5_encrypt(s)


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

    proxies = {
        "http": "http://localhost:8888",
        "https": "http://localhost:8888",
    }

    response = requests.post(url, headers=headers, data=data, proxies=proxies, verify=False)

    data = response.json()

    k = data['data']['k']
    captchaId = data['data']['captchaId']
    token = data['data']['token']
    front = data['data']['front'][0]
    bg = data['data']['bg'][0]
    print(k, captchaId, token, front, bg)
    return k, captchaId, token, front, bg


def main():
    tt = str(int(time.time() * 1000))
    # 第一次请求
    sign = get_sign(tt)
    k, captchaId, token, front, bg = get_auth_resp(tt, sign)

    # 第二次请求



if __name__ == '__main__':
    main()
