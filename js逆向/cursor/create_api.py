import base64
import hashlib
import json
import secrets
import threading
import time
import uuid
from urllib.parse import parse_qs, urlparse

from curl_cffi import requests
from Crypto.Random import get_random_bytes

from proxy import proxy_api
from random_api import r_api, n_api

from util.get_code_by_auth import get_code
from util.get_email import get_email
from util.get_fingerprint.get_f import get_f
from util.get_token import get_token

from util.uudi.uuid import ULID
from util.writer.ThreadSafeFileWriter import ThreadSafeFileWriter


class create_api:
    def __init__(self, root, on):
        self.wuid = ''
        self.pwd = r_api.get_random_password()
        self.name2 = r_api.get_random_last_name()
        self.name = r_api.get_random_first_name()
        self.on = on
        proxy_api.url = root.proxy_url.get()
        get_code.PROXIES = [root.proxy_url.get()]
        # self.session = requests.session()
        self.root = root
        self.email = ''
        self.email_name = ''
        self.num_ = 2
        self.uuid = ULID()
        self.proxy = proxy_api.p()
        self.p = ''
        self.tokne2 = None

    def get_token2(self):
        num = 3
        cf = None
        ua = None
        while num > 0:
            if self.root.captcha_pt.get() == 'capsolver':
                cf = get_token.get(self.root.captcha_api.get(), self.root.captcha_time.get())
            else:
                cf = get_token.get2(self.root.captcha_api.get(), self.root.captcha_time.get())
            if cf is not None and cf.get('solution') is not None and cf.get('solution').get('token') is not None:
                break
            num -= 1
        if cf is not None and cf.get('solution') is not None and cf.get('solution').get('token') is not None:
            self.token2 = cf.get('solution')
        else:
            raise Exception

    def start(self):
        try:
            self.p = self.proxy.http()
            # try:
            print(f"{self.email.split(':')[0]}开始注册！")
            if self.email == '':
                self.email = get_email.get(self.root.email_api.get())
                self.email_name = self.email.split(':')[0]
                self.root.update_data(self.root, self.on, 3, '获取邮箱成功!')
                print(self.email)
            self.root.update_data(self.root, self.on, 4, '正在获取token')
            self.root.update_data(self.root, self.on, 1, self.email.split(':')[0])
            self.root.update_data(self.root, self.on, 2, self.pwd)
            print(self.root.captcha_api.get())
            num = 3
            cf = None
            ua = None
            while num > 0:
                if self.root.captcha_pt.get() == 'capsolver':
                    cf = get_token.get(self.root.captcha_api.get(), self.root.captcha_time.get())
                else:
                    cf = get_token.get2(self.root.captcha_api.get(), self.root.captcha_time.get())
                if cf is not None and cf.get('solution') is not None and cf.get('solution').get('token') is not None:
                    break
                num -= 1
            if cf is not None and cf.get('solution') is not None and cf.get('solution').get('token') is not None:
                cf = cf.get('solution')
                self.root.update_data(self.root, self.on, 3, "获取token成功")
            else:
                self.root.update_data(self.root, self.on, 3, "获取token失败，正在重试")
                raise Exception
            if ua is None:
                ua = n_api.EnterpriseMacFingerprint().generate_mac_ua().get('userAgent')
            #            获取指纹
            threading.Thread(target=self.get_token2).start()
            session_id = self.uuid.generate()
            self.root.update_data(self.root, self.on, 4, "正在获取指纹")
            wuid = self.get_webkit(session_id)
            if not wuid:
                print(f"{self.email.split(':')[0]}获取指纹失败！")
                self.root.update_data(self.root, self.on, 3, "指纹获取失败")
                raise Exception
            else:
                print(f"{self.email.split(':')[0]}获取指纹成功!")
                self.root.update_data(self.root, self.on, 3, "指纹获取成功")

            self.wuid = wuid
            self.root.update_data(self.root, self.on, 4, "正在获取pending")
            p_token = self.reg_1(cf.get('token'), session_id)
            if p_token is not None:
                print(f"{self.email.split(':')[0]}获取pending_token成功!")
                self.root.update_data(self.root, self.on, 3, "获取pending成功")
            else:
                print(f"{self.email.split(':')[0]}获取pending_token失败!")
                self.root.update_data(self.root, self.on, 3, "获取pending失败")
                raise Exception
            num = 3
            code = None
            self.root.update_data(self.root, self.on, 4, "正在获取验证码")
            while num > 0:
                try:
                    code = get_code.get_code(self.email.split(':')[0], self.email.split(':')[2],
                                             self.email.split(':')[-1])
                except:
                    pass
                if code is not None:
                    break
                time.sleep(3)
                num -= 1
            if code is not None:
                print(f"{self.email.split(':')[0]}获取验证码成功{code}!")
                self.root.update_data(self.root, self.on, 3, f"验证码{code}")
            else:
                print(f"{self.email.split(':')[0]}获取验证码失败!")
                self.root.update_data(self.root, self.on, 3, "获取验证码失败")
                raise Exception
            num = 3
            cf = None
            ua = None
            self.root.update_data(self.root, self.on, 4, "二次获取token")
            while num > 0:
                if self.token2 is not None:
                    break
                time.sleep(3)
                num -= 1
            if self.token2 is not None:
                cf = self.token2
                self.root.update_data(self.root, self.on, 3, "二次获取token成功")
            else:
                self.root.update_data(self.root, self.on, 3, "二次获取token失败，正在重试")
                raise Exception
            self.root.update_data(self.root, self.on, 4, "正在查找重定向")
            r_url = self.submit_code(cf.get('token'), code, p_token, session_id)

            if r_url is not None:
                self.root.update_data(self.root, self.on, 3, "找到重定向")
                print(f"{self.email.split(':')[0]}找到重定向{r_url}!")
            else:
                self.root.update_data(self.root, self.on, 3, "没有找到重定向")
                print(f"{self.email.split(':')[0]}没有找到重定向{r_url}!")
                raise Exception
            self.root.update_data(self.root, self.on, 4, "正在查找cookie")
            cookie = self.call_back(r_url)
            if cookie is not None:
                self.root.update_data(self.root, self.on, 3, "找到cookie")
                print(f"{self.email.split(':')[0]}获取cookie成功{cookie}!")
            else:
                self.root.update_data(self.root, self.on, 3, "没有找到cookie")
                print(f"{self.email.split(':')[0]}获取cookie失败{cookie}!")
                raise Exception
            self.root.update_data(self.root, self.on, 4, "正在获取token")
            token_data = self.get_token(cookie)
            if token_data is not None:
                self.root.update_data(self.root, self.on, 4, "ok")
                self.root.update_data(self.root, self.on, 3, "注册成功")
            else:
                raise Exception
            data = {
                "email": self.email_name,
                "password": self.pwd,
                "cookie": token_data["full_cookie"],
                "token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
            }

            self.root.writer.write(f'{data.get("email")}----{data.get("password")}----{data.get("cookie")}'
                                   f'----{data.get("token")}\n')
            print('注册成功')
            self.root.yes += 1
            if self in self.root.p_list:
                self.root.p_list.remove(self)
        except:
            if self.num_ >= 0:
                self.num_ -= 1
                self.start()
            else:
                self.root.update_data(self.root, self.on, 3, f"注册失败")
                self.root.update_data(self.root, self.on, 4, f"已终止")
                if self in self.root.p_list:
                    self.root.p_list.remove(self)

    def generate_code_verifier(self):
        """生成随机的32字节数据并进行base64url编码作为code_verifier"""
        random_bytes = secrets.token_bytes(32)
        code_verifier = base64.urlsafe_b64encode(random_bytes).decode("utf-8")
        # 移除填充字符
        code_verifier = code_verifier.rstrip("=")
        return code_verifier

    def generate_code_challenge(self, code_verifier):
        """根据code_verifier计算code_challenge"""
        # 计算SHA256哈希
        sha256_hash = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        # 进行base64url编码
        code_challenge = base64.urlsafe_b64encode(sha256_hash).decode("utf-8")
        # 移除填充字符
        code_challenge = code_challenge.rstrip("=")
        return code_challenge

    def extract_cookie(self, cookie_string: str) -> str:
        """从完整cookie字符串中提取纯cookie值，去掉前缀和后缀"""
        try:
            # 去掉前缀 "WorkosCursorSessionToken="
            if "WorkosCursorSessionToken=" in cookie_string:
                cookie_string = cookie_string.replace("WorkosCursorSessionToken=", "")

            # 去掉后缀 "; Path=/; HttpOnly; Secure; SameSite=Lax"
            if "; Path=" in cookie_string:
                cookie_string = cookie_string.split("; Path=")[0]

            return cookie_string
        except Exception as e:
            return cookie_string  # 返回原始字符串作为后备

    def get_token(self, cookies_str):
        # 生成随机参数
        random_verifier = self.generate_code_verifier()
        random_challenge = self.generate_code_challenge(random_verifier)
        random_uuid = str(uuid.uuid4())

        # 从cookies字符串中提取cookie值
        session_token = self.extract_cookie(cookies_str)

        # 发送认证回调请求
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://www.cursor.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": f"https://www.cursor.com/cn/loginDeepControl?challenge={random_challenge}&uuid={random_uuid}&mode=login",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }

        cookies = {
            "NEXT_LOCALE": "cn",
            "WorkosCursorSessionToken": session_token,
        }

        url = "https://www.cursor.com/api/auth/loginDeepCallbackControl"
        data = {
            "uuid": random_uuid,
            "challenge": random_challenge,
        }

        # 发送请求初始化验证过程
        response = self.send_post3(url, data, headers, cookies)

        print('开始获取token')
        # 开始轮询获取token
        poll_url = f"https://api2.cursor.sh/auth/poll?uuid={random_uuid}&verifier={random_verifier}"

        poll_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Cursor/0.48.6 Chrome/132.0.6834.210 Electron/34.3.4 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua-platform": '"Windows"',
            "x-ghost-mode": "true",
            "x-new-onboarding-completed": "false",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132"',
            "sec-ch-ua-mobile": "?0",
            "origin": "vscode-file://vscode-app",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "accept-language": "zh-CN",
            "priority": "u=1, i",
        }

        max_attempts = 15  # 最多尝试15次
        retry_interval = 5  # 每5秒尝试一次

        for attempt in range(max_attempts):
            try:

                poll_response = self.send_get2(poll_url, poll_headers)

                # 直接尝试解析响应体，不依赖状态码
                try:
                    response_text = poll_response.text

                    response_data = json.loads(response_text)
                    if "accessToken" in response_data:

                        access_token = response_data.get("accessToken")
                        auth_id = response_data.get("authId")

                        if access_token and auth_id:
                            # 从authId中提取user_id部分
                            user_id = auth_id.split("|")[1]
                            # 构建cursor_cookie格式
                            full_cookie = f"{user_id}%3A%3A{access_token}"
                            return {
                                "access_token": access_token,
                                "refresh_token": response_data.get("refreshToken"),
                                "full_cookie": full_cookie,
                            }
                        else:
                            continue
                    else:
                        pass
                except json.JSONDecodeError:
                    print('error')
                except Exception as e:
                    print('error')



            except Exception as e:
                print('error')

            # 等待再次尝试
            time.sleep(retry_interval)

        return None

    def call_back(self, r_url: str):
        parsed = urlparse(r_url)
        code = parse_qs(parsed.query)["code"][0]
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        # 如果有WebKit指纹，添加到Cookie
        if self.wuid:
            headers["Cookie"] = f"__wuid={self.wuid}"
            # logger.debug("已将WebKit指纹添加到callback请求的Cookie")

        callback_url = "https://www.cursor.com/api/auth/callback"
        params = {"code": code, "state": "%7B%22returnTo%22%3A%22%2Fsettings%22%7D"}
        rps = self.send_get(callback_url, headers, params)
        cookies = rps.headers.get("set-cookie")
        return cookies

    # 提交验证码
    def submit_code(self, token, code, pending_token, session_id):
        boundary = "----WebKitFormBoundaryqEBf0rEYwwb9aUoF"
        headers = {
            "accept": "text/x-component",
            "content-type": f"multipart/form-data; boundary={boundary}",
            "next-action": "e75011da58d295bef5aa55740d0758a006468655",
            "origin": "https://authenticator.cursor.sh",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        # 如果有WebKit指纹，添加到Cookie
        if self.wuid:
            headers["Cookie"] = f"__wuid={self.wuid}"
            # logger.debug("已将WebKit指纹添加到验证请求的Cookie")

        params = {
            "email": self.email_name,
            "pending_authentication_token": pending_token,
            "state": "%7B%22returnTo%22%3A%22%2Fsettings%22%7D",
            "redirect_uri": "https://cursor.com/api/auth/callback",
            "authorization_session_id": session_id,
        }
        form_data = self.build_verify_form(
            boundary=boundary,
            email=self.email_name,
            token=token,
            code=code,
            pending_token=pending_token,
        )
        rps = self.send_post2("https://authenticator.cursor.sh/email-verification", form_data, headers, params)
        redirect_url = rps.headers.get("x-action-redirect")
        if not redirect_url:
            return None
        return redirect_url

    def build_verify_form(self,
                          boundary: str, email: str, token: str, code: str, pending_token: str
                          ) -> str:
        """构建验证表单数据"""
        fields = {
            "1_pending_authentication_token": pending_token,
            "1_email": email,
            "1_state": '{"returnTo":"/settings"}',
            "1_redirect_uri": "https://cursor.com/api/auth/callback",
            "1_bot_detection_token": token,
            "1_code": code,
            "0": '["$K1"]',
        }

        form_data = []
        for key, value in fields.items():
            form_data.append(f"--{boundary}")
            form_data.append(f'Content-Disposition: form-data; name="{key}"')
            form_data.append("")
            form_data.append(value)

        form_data.append(f"--{boundary}--")
        return "\r\n".join(form_data)

    # 第一次注册
    def reg_1(self, token, session_id):
        boundary = "----WebKitFormBoundary2rKlvTagBEhneWi3"
        headers = {
            "accept": "text/x-component",
            "next-action": "770926d8148e29539286d20e1c1548d2aff6c0b9",
            "content-type": f"multipart/form-data; boundary={boundary}",
            "origin": "https://authenticator.cursor.sh",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        if self.wuid:
            headers["Cookie"] = f"__wuid={self.wuid}"

        params = {
            "first_name": self.name,
            "last_name": self.name2,
            "email": self.email_name,
            "state": "%7B%22returnTo%22%3A%22%2Fsettings%22%7D",
            "redirect_uri": "https://cursor.com/api/auth/callback",
            "authorization_session_id": session_id,
        }
        form_data, cursor_password = self.build_register_form(
            boundary, self.email_name, token, self.name, self.name2
        )
        rps = self.send_post2('https://authenticator.cursor.sh/sign-up/password',
                              form_data, headers, params)
        print(rps.text)
        pending_token = self._extract_auth_token(rps.text)
        return pending_token

    def _extract_auth_token(self,
                            response_text: str
                            ) -> str | None:
        """从响应文本中提取pending_authentication_token"""
        res = response_text.split("\n")
        # logger.debug(f"开始提取 auth_token，响应行数: {len(res)}")
        try:
            for i, r in enumerate(res):
                if r.startswith("0:"):
                    # logger.debug(f"在第 {i+1} 行找到匹配")
                    data = json.loads(r.split("0:")[1])
                    auth_data = data[1][0][0][1]["children"][1]["children"][1][
                        "children"
                    ][1]["children"][0]
                    params_str = auth_data.split("?")[1]
                    params_dict = json.loads(params_str)
                    token = params_dict["pending_authentication_token"]
                    # logger.debug(f"方法2提取成功: {token[:10]}...")
                    return token
        except Exception:
            # logger.error(f"提取token失败: {str(e)}")
            # logger.debug("响应内容预览:", response_text[:200])
            ...

        return None

    def build_register_form(
            self,
            boundary: str, email: str, token: str, first_name: str, last_name: str
    ) -> tuple[str, str]:
        """构建注册表单数据，返回(form_data, password)"""
        password = self.pwd
        fields = {
            "1_state": '{"returnTo":"/settings"}',
            "1_redirect_uri": "https://cursor.com/api/auth/callback",
            "1_bot_detection_token": token,
            "1_first_name": first_name,
            "1_last_name": last_name,
            "1_email": email,
            "1_password": password,
            "1_intent": "sign-up",
            "0": '["$K1"]',
        }

        form_data = []
        for key, value in fields.items():
            form_data.append(f"--{boundary}")
            form_data.append(f'Content-Disposition: form-data; name="{key}"')
            form_data.append("")
            form_data.append(value)

        form_data.append(f"--{boundary}--")
        return "\r\n".join(form_data), password

    def generate_random_hash(self):
        """生成随机的指纹哈希"""
        random_bytes = get_random_bytes(32)
        random_hex = random_bytes.hex()
        return random_hex

    def get_webkit(self, session_id):
        wuid = None
        finger_hash = self.generate_random_hash()
        url = f"https://authenticator.cursor.sh/?client_id=client_01GS6W3C96KW4WRS6Z93JCE2RJ&redirect_uri=https%3A%2F%2Fcursor.com%2Fapi%2Fauth%2Fcallback&response_type=code&state=%257B%2522returnTo%2522%253A%2522%252Fsettings%2522%257D&authorization_session_id={session_id}"
        payload_list = f'["{finger_hash}"]'
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
        rps = self.send_post(url, payload_list, headers)

        for line in rps.text.split('\n'):
            if line.startswith("1:"):
                try:
                    json_data = json.loads(line.replace("1:", ""))
                    wuid = json_data.get("payload")
                    # logger.debug(f"成功提取WebKit指纹: {wuid[:10]}...")
                    break
                except Exception:
                    # logger.error(f"解析WebKit响应失败: {str(e)}")
                    ...
        return wuid

    def send_post(self, url, data, header):
        try:
            rps = requests.post(url=url, data=data, headers=header, impersonate='chrome124', proxies=self.p,
                                verify=False)
            return rps
        except Exception as e:
            print(e)
            time.sleep(1)
            self.p = self.proxy.http()
            return self.send_post(url, data, header)

    def send_post2(self, url, data, header, params, ):
        try:
            rps = requests.post(url=url, data=data, headers=header
                                , params=params, impersonate='chrome124', proxies=self.p, verify=False)
            return rps
        except:
            time.sleep(1)
            self.p = self.proxy.http()
            return self.send_post2(url, data, header, params)

    def send_post3(self, url, data, header, cookies):
        try:
            rps = requests.post(url=url, json=data, headers=header
                                , cookies=cookies, impersonate='chrome124', proxies=self.p, verify=False)
            return rps
        except:
            time.sleep(1)
            self.p = self.proxy.http()
            return self.send_post3(url, data, header, cookies)

    def send_get(self, url, header, params):
        try:
            rps = requests.get(url=url, headers=header
                               , params=params, impersonate='chrome124', proxies=self.p, verify=False,
                               allow_redirects=False, )
            return rps
        except:
            time.sleep(1)
            self.p = self.proxy.http()
            return self.send_get(url, header, params)

    def send_get2(self, url, header):
        try:
            rps = requests.get(url=url, headers=header
                               , impersonate='chrome124', proxies=self.p, verify=False)
            return rps
        except:
            time.sleep(1)
            self.p = self.proxy.http()
            return self.send_get2(url, header)
