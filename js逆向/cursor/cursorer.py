import json
import time
import requests
from curl_cffi import requests as cffi_requests
from Crypto.Random import get_random_bytes
from core.cookie import get_session_user_id
from utils.captcha import get_turnstile_token


class Cursor:
    def __init__(self, proxy=None):
        # 邮箱
        self.username = 'tlc77htpwh@outlook.jp'
        self.password = 'z0ftqgidrm4nnxek'
        self.session = cffi_requests.Session()  # 使用 curl_cffi 替代标准 requests
        self.proxy = proxy  # 支持传入代理（格式：{"http": "http://user:pass@ip:port", "https": ...}）

        self.session.headers.update({
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://www.cursor.com/ja",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"131\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        })

        self.session.cookies.update({
            'IndrX2ZuSmZramJSX0NIYUZoRzRzUGZ0cENIVHpHNXk0VE0ya2ZiUkVzQU14X2Fub255bW91c1VzZXJJZCI%3D': get_session_user_id(),
            'NEXT_LOCALE': 'ja',
        })

    def get_first_request(self):
        """
        请求登录页，获取必要 cookie 和 cf_clearance
        """
        session_id = get_session_user_id()
        cookies = self.get_cookies(session_id)
        self.session.cookies.update(cookies)
        print('当前 cookies: ', self.session.cookies.get_dict())

        # 执行登录,获取token
        token = self.login()
        print(token)
        return None

    def build_login_form(self, boundary: str, email: str, password: str, token: str):
        """
        构建登录表单数据，模仿 create_api 的 build_verify_form
        """
        fields = {
            '1_bot_detection_token': token,
            '1_email': email,
            '1_password': password,
            '1_intent': 'password',
            '1_redirect_uri': 'https://cursor.com/api/auth/callback',
            '0': '["$K1"]',
        }

        form_data = []
        for key, value in fields.items():
            form_data.append(f"--{boundary}")
            form_data.append(f'Content-Disposition: form-data; name="{key}"')
            form_data.append("")
            form_data.append(value)

        form_data.append(f"--{boundary}--")
        return "\r\n".join(form_data)

    def get_redirect(self, response):
        """
        处理重定向请求
        :return:
        """
        # 处理重定向

        while response.status_code != 200:
            redirect_url = response.headers.get('Location') or response.headers.get('x-action-redirect')

            print(f"检测到 303 重定向，目标 URL: {redirect_url}")

            response = self.session.get(
                redirect_url,
                impersonate="chrome131",
                proxies=self.proxy,
                verify=False,
            )

            print('当前重定向状态：', response.status_code)
            print('当前重定向url：', response.url)
            print('当前重定向cookies：', response.cookies.get_dict())
            # print(response.text)
            print('--------------------')
        return response.cookies.get_dict()['WorkosCursorSessionToken']

    def login(self):
        """
        执行登录，模仿 create_api 的 multipart 表单处理
        """
        self.session.cookies.update({
            "_dd_s": f"rum=0&expire={str(int(time.time() * 1000) + 2000)}"
        })
        print("当前 cookies: ", self.session.cookies.get_dict())

        boundary = "----WebKitFormBoundaryqEBf0rEYwwb9aUoF"  # 与 create_api 一致
        headers = {
            'accept': 'text/x-component',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'next-action': 'ff6a0c8c51b187aaeb0ed2f8f534a41dca975e44',
            'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22(root)%22%2C%7B%22children%22%3A%5B%22(sign-in)%22%2C%7B%22children%22%3A%5B%22password%22%2C%7B%22children%22%3A%5B%22__PAGE__%3F%7B%5C%22email%5C%22%3A%5C%222480419172%40qq.com%5C%22%2C%5C%22redirect_uri%5C%22%3A%5C%22https%3A%2F%2Fcursor.com%2Fapi%2Fauth%2Fcallback%5C%22%7D%22%2C%7B%7D%2C%22%2Fpassword%3Femail%3D2480419172%2540qq.com%26redirect_uri%3Dhttps%253A%252F%252Fcursor.com%252Fapi%252Fauth%252Fcallback%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
            'origin': 'https://authenticator.cursor.sh',
            'referer': 'https://authenticator.cursor.sh/password?email=2480419172%40qq.com&redirect_uri=https%3A%2F%2Fcursor.com%2Fapi%2Fauth%2Fcallback',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'content-type': f'multipart/form-data; boundary={boundary}',
        }

        params = {
            'email': self.username,
            'redirect_uri': 'https://cursor.com/api/auth/callback',
        }

        # 构建 multipart 表单数据
        form_data = self.build_login_form(
            boundary=boundary,
            email=self.username,
            password=self.password,
            token=get_turnstile_token()
        )

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = self.session.post(
                    'https://authenticator.cursor.sh/password',
                    params=params,
                    data=form_data,  # 使用 data 参数发送手动构建的表单
                    headers=headers,
                    impersonate="chrome131",
                    proxies=self.proxy,
                    verify=False,
                    allow_redirects=True
                )

                if response.status_code == 303:
                    # 重定向
                    token = self.get_redirect(response)
                    return token
                elif response.status_code == 200:
                    # 提取数据
                    # 提取 JSON 数据
                    json_data = None
                    for line in response.text.split('\n'):
                        if line.startswith('1:'):
                            json_str = line[2:]  # 移除 '1:' 前缀
                            try:
                                json_data = json.loads(json_str)
                                print("提取的 JSON 数据:", json_data)
                                break
                            except json.JSONDecodeError as e:
                                print(f"JSON 解析失败: {e}")

                    return json_data
                else:
                    print(f"登录失败，状态码: {response.status_code}，重试...")
                    retry_count += 1
                    time.sleep(2)

            except Exception as e:
                print(f"登录请求失败: {e}")
                retry_count += 1
                time.sleep(2)

        raise Exception("登录失败，请检查网络、cookie 或 CAPTCHA 配置")

    def get_cookies(self, session_id):
        """
        获取 __wuid cookie
        """
        url = f'https://authenticator.cursor.sh/?client_id=client_01GS6W3C96KW4WRS6Z93JCE2RJ&redirect_uri=https%3A%2F%2Fcursor.com%2Fapi%2Fauth%2Fcallback&response_type=code&state=%257B%2522returnTo%2522%253A%2522%252Fsettings%2522%257D&authorization_session_id={session_id}'
        random_bytes = get_random_bytes(32)
        finger_hash = random_bytes.hex()
        payload = f'["{finger_hash}"]'

        headers = {
            "next-action": "a67eb6646e43eddcbd0d038cbee664aac59f5a53",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-full-version": '"127.0.6533.120"',
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform-version": '"15.0.0"',
            "content-type": "text/plain;charset=UTF-8",
        }

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = self.session.post(
                    url=url,
                    data=payload,
                    headers=headers,
                    impersonate="chrome131",
                    proxies=self.proxy,
                    verify=False
                )

                print("get_cookies 响应:", response.status_code)
                print("get_cookies 内容:", response.text)

                wuid = None
                for line in response.text.split('\n'):
                    if line.startswith("1:"):
                        try:
                            json_data = json.loads(line.replace("1:", ""))
                            wuid = json_data.get("payload")
                            print(f"成功获取 __wuid: {wuid[:30]}...")
                            break
                        except Exception as e:
                            print(f"解析 __wuid 失败: {e}")

                cookies = response.cookies.get_dict()
                if wuid:
                    cookies['__wuid'] = wuid
                return cookies

            except Exception as e:
                print(f"获取 __wuid 失败: {e}")
                retry_count += 1
                time.sleep(2)

        raise Exception("获取 __wuid 失败，请检查网络或配置")
