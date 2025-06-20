import json
import random
import string
import time
import uuid

import ddddocr
import execjs
import requests

from 滑块练习.云片.Tujian import base64_api


class YunPianSpider:
    def __init__(self):
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        cookies = {
            "_ga_ESVMH6YSPX": "GS2.1.s1750331949$o1$g0$t1750331949$j60$l0$h0",
            "__wksid": "n-AB7AB4CEED9A4B47BAE00C1169D09734",
            "_gid": "GA1.2.943299681.1750331950",
            "_ga_B8H0JYR4RL": "GS2.1.s1750331950$o1$g0$t1750331950$j60$l0$h0",
            "_ga": "GA1.1.1874583663.1750331949",
            "MEIQIA_TRACK_ID": "2yiz0S2n1Xoyk7rK1IHSeDkKpuk",
            "MEIQIA_VISIT_ID": "2yiz0TQHAnC9sMFWsJzrJxrg3Ls"
        }
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)
        self.uuid = str(uuid.uuid4())
        self.key = self.generate_16_char_string()
        self.iv = self.generate_16_char_string()

    def get_cb(self, length=11):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def get_res_e(self, e):
        """获取i,k"""
        e = json.dumps(e)
        res_e = execjs.compile(
            open('./loader.js', 'r', encoding='utf-8').read()).call(
            "get_e", e, self.key, self.iv)
        return res_e

    def generate_16_char_string(self):
        chars = string.ascii_letters + string.digits  # 包含大小写字母和数字
        return ''.join(random.choice(chars) for _ in range(16))

    def get_base_info(self):
        """获取基础参数"""
        url = "https://captcha.yunpian.com/v1/jsonp/captcha/get"
        e = {
            "browserInfo": [
                {
                    "key": "userAgent",
                    "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
                },
                {
                    "key": "language",
                    "value": "zh-CN"
                },
                {
                    "key": "hardware_concurrency",
                    "value": 16
                },
                {
                    "key": "resolution",
                    "value": [
                        1707,
                        960
                    ]
                },
                {
                    "key": "navigator_platform",
                    "value": "Win32"
                }
            ],
            "nativeInfo": None,
            "additions": {},
            "options": {
                "sdk": "https://www.yunpian.com/static/official/js/libs/riddler-sdk-0.2.2.js",
                "sdkBuildVersion": "1.5.0(2021111001)",
                "hosts": "https://captcha.yunpian.com"
            },
            "address": "https://www.yunpian.com",
            "yp_riddler_id": self.uuid
        }
        res_e = self.get_res_e(e)

        params = {
            "cb": self.get_cb(),
            "i": res_e['i'],
            "k": res_e['k'],
            "captchaId": "974cd565f11545b6a5006d10dc324281"
        }
        response = self.session.get(url, params=params)

        data = json.loads(response.text[8:-1])
        bg = data["data"]["bg"]
        front = data["data"]["front"]
        width = int(int(data["data"]["width"]) / 1.57)
        sliderWidth = int(int(data["data"]["sliderWidth"]) / 1.57)
        token = data["data"]["token"]
        return bg, front, width, sliderWidth, token

    def get_token(self):
        """获取token"""
        url = "https://captcha.yunpian.com/v1/jsonp/captcha/get"
        e = {
            "browserInfo": [
                {
                    "key": "userAgent",
                    "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
                },
                {
                    "key": "language",
                    "value": "zh-CN"
                },
                {
                    "key": "hardware_concurrency",
                    "value": 16
                },
                {
                    "key": "resolution",
                    "value": [
                        1707,
                        960
                    ]
                },
                {
                    "key": "navigator_platform",
                    "value": "Win32"
                }
            ],
            "nativeInfo": None,
            "additions": {},
            "options": {
                "sdk": "https://www.yunpian.com/static/official/js/libs/riddler-sdk-0.2.2.js",
                "sdkBuildVersion": "1.5.0(2021111001)",
                "hosts": "https://captcha.yunpian.com"
            },
            "address": "https://www.yunpian.com",
            "yp_riddler_id": str(uuid.uuid4())
        }
        res_e = self.get_res_e(e)
        params = {
            "cb": self.get_cb(),
            "i": res_e['i'],
            "k": res_e['k'],
            "captchaId": "974cd565f11545b6a5006d10dc324281"
        }
        response = self.session.get(url, params=params)

        data = json.loads(response.text[8:-1])
        return data['data']['token']

    def get_distance(self, bg_url, fg_url):
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
        # print(slide_distance)
        return int(slide_distance / 1.45)

    def generate_drag_trajectory(self, distance, width, sliderWidth, start_x=100, start_y=200, raw_step=5, delay=0.01,
                                 max_points_amount=50):
        """
        生成拖动轨迹，返回格式为 [x, y, dt] 的数组，最多 max_points_amount 个点
        """
        raw_x = start_x
        raw_timestamp = time.time()
        trajectory = []

        # 原始轨迹（细粒度）
        for dx in range(0, distance + 1, raw_step):
            current_x = start_x + dx
            current_y = start_y + random.randint(-2, 2)  # 上下抖动
            dt = int((time.time() - raw_timestamp) * 1000)  # 毫秒
            trajectory.append([current_x, current_y, dt])
            time.sleep(delay)

        # 降采样为最多 max_points_amount 个点
        if len(trajectory) > max_points_amount:
            total = len(trajectory)
            step = (total - 1) / (max_points_amount - 1)
            indices = [round(i * step) for i in range(max_points_amount)]
            trajectory = [trajectory[i] for i in indices]
        # 获取distanceX

        distanceX = (width - sliderWidth) * (distance / (width - 42)) / width

        return trajectory, distanceX

    def parse_traceData(self, slide_distance):
        start_x = random.randint(1100, 1120)
        start_y = random.randint(1880, 1890)
        start_t = random.randint(50, 60)
        traceData = [[start_x, start_y, start_t]]
        x = 0
        t = 0
        while x < slide_distance:
            x += random.randint(1, 5)
            y = random.randint(-1, 1)
            t += random.randint(10, 20)
            point_x = start_x + x
            point_y = start_y + y
            point_t = start_t + t
            if x >= slide_distance:
                point_x = start_x + slide_distance
                trace = [point_x, point_y, point_t]
                traceData.append(trace)
                break
            trace = [point_x, point_y, point_t]
            traceData.append(trace)
        for i in range(5):
            t += random.randint(10, 20)
            point_t = start_t + t
            trace = [point_x, point_y, point_t]
            traceData.append(trace)
        return traceData

    def verify_code(self, track, distanceX, token):
        """验证"""
        url = "https://captcha.yunpian.com/v1/jsonp/captcha/verify"
        e = {
            "points": track,
            "distanceX": float(distanceX),
            "address": "https://www.yunpian.com",
            "yp_riddler_id": self.uuid
        }
        res_e = self.get_res_e(e)
        params = {
            "cb": "a0pd0engbfs",
            "i": res_e['i'],
            "k": res_e['k'],
            "token": token,
            "captchaId": "974cd565f11545b6a5006d10dc324281"
        }
        response = self.session.get(url, params=params)

        data = json.loads(response.text[8:-1])
        print("res", data)
        try:
            return data['data']['result']
        except:
            return False

    def main(self):
        """开始"""
        # 获取基础参数
        # 先获取token
        bg, front, width, sliderWidth, token = self.get_base_info()
        # 获取滑动距离
        slide_distance = self.get_distance(bg, front)
        # 获取轨迹
        track, distanceX = self.generate_drag_trajectory(slide_distance, width, sliderWidth, start_x=1018, start_y=1962)
        print("轨迹数组", track)
        print("distanceX", distanceX)
        track = self.parse_traceData(slide_distance)
        # 提交验证
        res = self.verify_code(track, distanceX, token)
        if res:
            print('验证成功')
        else:
            print('验证失败')
