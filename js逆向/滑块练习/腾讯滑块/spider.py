import base64
import json
import urllib

import execjs
import requests

from js逆向.滑块练习.腾讯滑块.Tujian import base64_api


class TxSpider:
    """
    腾讯滑块验证
    """

    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://cloud.tencent.com/",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.cookies = {
            "qcmainCSRFToken": "r1e8sEw6mgg",
            "intl": "",
            "uin": "100023630441",
            "skey": "KfvsiNdJl-uyye4GUWLyMa9uyN-bEn883-zLegkRgGQ_"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)

    def get_encode_ua(self):
        # 去除 Unicode 字符中大于 0x00FF 的字符
        cleaned_ua = ''.join(c for c in self.headers['User-Agent'] if ord(c) <= 0x00FF)

        # Base64 编码
        b64_encoded = base64.b64encode(cleaned_ua.encode()).decode()

        # URL 编码
        url_encoded = urllib.parse.quote(b64_encoded)

        return url_encoded

    def get_prehandle(self):
        """前置，获取基础的参数"""
        url = "https://turing.captcha.qcloud.com/cap_union_prehandle"
        # 获取ua
        ua = self.get_encode_ua()
        print(f"ua:::{ua}")

        params = {
            "aid": "199999861",
            "protocol": "https",
            "accver": "1",
            "showtype": "popup",
            "ua": ua,
            "noheader": "1",
            "fb": "1",
            "aged": "0",
            "enableAged": "0",
            "enableDarkMode": "0",
            "grayscale": "1",
            "clientype": "2",
            "cap_cd": "",
            "uid": "",
            "lang": "zh-cn",
            "entry_url": "https://cloud.tencent.com/product/captcha",
            "elder_captcha": "0",
            "js": "/tcaptcha-frame.c055d939.js",
            "login_appid": "",
            "wb": "2",
            "subsid": "17",
            "callback": "_aq_70462",
            "sess": ""
        }
        response = self.session.get(url, params=params)

        data = response.text

        data = data[10:-1]
        data = json.loads(data)
        print(data)
        # 获取参数内容
        host = 'https://turing.captcha.qcloud.com'
        bg_img_url = host + data["data"]["dyn_show_info"]["bg_elem_cfg"]["img_url"]  # 背景图
        front_img_url = host + data["data"]["dyn_show_info"]["sprite_url"]  # 前图
        y = data["data"]["dyn_show_info"]["fg_elem_list"][1]["init_pos"][1]  # y值
        sess = data['sess']  # 验证参数
        prefix = data["data"]["comm_captcha_cfg"]["pow_cfg"]["prefix"]  # prefix
        md = data["data"]["comm_captcha_cfg"]["pow_cfg"]["md5"]  # prefix
        return bg_img_url, front_img_url, sess, y, prefix, md

    def verify_slide(self, sess, track, y, prefix, md):
        """验证滑块"""
        url = "https://turing.captcha.qcloud.com/cap_union_new_verify"

        collect = execjs.compile(
            open("D:\projects\Spider-WebUnlocker\js逆向\滑块练习\腾讯滑块\loader.js", encoding="utf-8").read()).call(
            'get_collection')
        eks = execjs.compile(
            open("D:\projects\Spider-WebUnlocker\js逆向\滑块练习\腾讯滑块\loader.js", encoding="utf-8").read()).call(
            'get_eks')
        print('collect:::', collect)
        print('eks:::', eks)
        ans = [
            {
                "elem_id": 1,
                "type": "DynAnswerType_POS",
                "data": [track, y]  # 不用字符串，而是直接传数组
            }
        ]
        t = {
            "target": md,
            "nonce": prefix
        }
        anss = execjs.compile(
            open("D:\projects\Spider-WebUnlocker\js逆向\滑块练习\腾讯滑块\loader2.js", encoding="utf-8").read()).call(
            'get_ans' , t)
        print('anss' , anss)

        data = {
            "collect": collect,
            "tlg": len(collect),
            "eks": eks,
            "sess": sess,
            "ans": json.dumps(ans),
            "pow_answer": prefix + str(anss['ans']),
            "pow_calc_time": str(anss['duration'])
        }
        # 验证参数
        print('验证参数' , data)
        response = self.session.post(url, data=data)

        print("验证结果", response.text)

    def cal_track(self, bg_img):
        """计算轨迹"""
        print(bg_img)
        with open('bg_img.png', 'wb') as f:
            f.write(requests.get(bg_img).content)
        # 计算缺口
        x = base64_api(uname='jiaoxingk', pwd='Cs5201314dd', img='bg_img.png', typeid=33)
        print("x:::", x)
        return int(x) - 20

    def start(self):
        """滑块验证入口"""
        # 前置prehandle函数，获取基础的信息
        bg_img_url, front_img_url, sess, y, prefix, md = self.get_prehandle()
        # 计算轨迹
        track = self.cal_track(bg_img_url)
        # 验证滑块
        self.verify_slide(sess, track, y, prefix, md)
