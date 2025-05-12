import os
import time
import json
import secrets
import sqlite3
import requests
import urllib.parse
from pathlib import Path
from curl_cffi import requests as cffi_requests
import uuid

from utils import (
    EMOJI, logger, generate_random_password, generate_random_name,
    generate_code_verifier, generate_code_challenge, extract_cookie,
    generate_random_hash, generate_random_uuid, save_account_info,
    extract_json_from_response, parse_url_params, get_session_user_id,
    process_token
)
from email_service import EmailService
from captcha_service import CaptchaService


class CursorRegister:
    """Cursor注册客户端"""

    def __init__(self,
                 email_api_type='mail.td',
                 email_api_key=None,
                 captcha_api_type='capsolver',
                 captcha_api_key=None,
                 proxy=None,
                 use_mock=False):
        """
        初始化Cursor注册客户端
        
        参数:
            email_api_type: 邮箱API类型
            email_api_key: 邮箱API密钥
            captcha_api_type: 验证码API类型
            captcha_api_key: 验证码API密钥
            proxy: 代理设置，格式为 "http://user:pass@ip:port" 或 {"http": "...", "https": "..."}
            use_mock: 是否使用模拟模式（用于测试）
        """
        self.email_service = EmailService(
            api_type=email_api_type,
            api_key=email_api_key
        )

        # 使用mock模式还是正常模式
        captcha_type = 'mock' if use_mock else captcha_api_type
        self.captcha_service = CaptchaService(
            api_type=captcha_type,
            api_key=captcha_api_key
        )

        # 初始化curl_cffi会话
        self.session = cffi_requests.Session()
        self.session.headers.update({
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"131\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        })

        self.session.cookies.update({
            'IndrX2ZuSmZramJSX0NIYUZoRzRzUGZ0cENIVHpHNXk0VE0ya2ZiUkVzQU14X2Fub255bW91c1VzZXJJZCI%3D': get_session_user_id(),
            'NEXT_LOCALE': 'ja',
        })

        # 处理代理格式
        self.proxy = None
        if proxy:
            if isinstance(proxy, str):
                self.proxy = {
                    "http": proxy,
                    "https": proxy
                }
            else:
                self.proxy = proxy

        # 用户信息
        self.email = None
        self.email_address = None
        self.password = generate_random_password()
        self.first_name, self.last_name = generate_random_name()

        # 会话信息
        self.session_id = None
        self.auth_token = None
        self.pending_token = None
        self.verification_code = None
        self.access_token = None
        self.refresh_token = None
        self.cookie = None

        # 其他参数
        self.webkit_id = None
        self.use_mock = use_mock
        logger.info(f"{EMOJI['INFO']} 初始化Cursor注册客户端成功")

    def register(self):
        """
        执行Cursor注册流程
        
        返回:
            dict: 注册结果
        """
        try:
            logger.info(f"{EMOJI['START']} 开始Cursor账号注册流程")

            # 步骤1: 获取邮箱
            logger.info(f"{EMOJI['MAIL']} 正在获取邮箱...")
            self.email = self.email_service.get_email()

            if not self.email:
                return {"success": False, "message": "获取邮箱失败"}

            self.email_address = self.email.split(':')[0]

            # 步骤2: 获取Webkit ID
            logger.info(f"{EMOJI['INFO']} 正在获取Webkit ID...")
            self.session_id = generate_random_uuid()
            self.webkit_id = self._get_webkit_id()

            if not self.webkit_id:
                return {"success": False, "message": "获取Webkit ID失败"}
            else:
                logger.info(f"Webkit ID: {self.webkit_id}")

            # 步骤3: 提交注册表单
            logger.info(f"{EMOJI['FORM']} 正在提交注册表单...")
            token = self.captcha_service.get_turnstile_token()
            if not token:
                return {"success": False, "message": "获取验证码token失败"}
            logger.info(f"获取到的验证token：{token}")

            self.pending_token = self._submit_registration(token)
            if not self.pending_token:
                return {"success": False, "message": "提交注册表单失败"}

            # 步骤4: 获取邮箱验证码
            logger.info(f"{EMOJI['CODE']} 正在获取验证码...")
            self.verification_code = self.email_service.get_verification_code()
            if not self.verification_code:
                return {"success": False, "message": "获取邮箱验证码失败"}

            # 步骤5: 验证邮箱
            logger.info(f"{EMOJI['VERIFY']} 正在验证邮箱...")
            token2 = self.captcha_service.get_turnstile_token()
            if not token2:
                return {"success": False, "message": "获取第二次验证码token失败"}

            redirect_url = self._verify_email(token2)
            if not redirect_url:
                return {"success": False, "message": "验证邮箱失败"}

            # 步骤6: 处理回调
            logger.info(f"{EMOJI['KEY']} 正在处理登录回调...")
            self.cookie = self._handle_callback(redirect_url)
            if not self.cookie:
                return {"success": False, "message": "处理回调失败"}

            print('获取：WorkosCursorSessionToken: ', self.cookie)

            # 步骤7: 获取token
            logger.info(f"{EMOJI['KEY']} 正在获取访问token...")
            token_data = self._get_token()
            if not token_data:
                return {"success": False, "message": "获取token失败"}

            # 保存账号信息
            if not save_account_info(
                    self.email_address,
                    self.password,
                    token_data["access_token"],
                    token_data["refresh_token"],
                    self.cookie
            ):
                logger.warning(f"{EMOJI['WARNING']} 保存账号信息失败，但不影响注册过程")

            # 返回结果
            logger.info(f"{EMOJI['DONE']} Cursor账号注册成功！")
            return {
                "success": True,
                "message": f"Cursor账号注册成功！邮箱: {self.email_address}",
                "email": self.email_address,
                "password": self.password,
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "cookie": self.cookie
            }

        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 注册过程中发生错误: {str(e)}")
            return {"success": False, "message": f"注册过程中发生错误: {str(e)}"}

    def _get_webkit_id(self):
        """获取Webkit ID"""
        try:
            url = f"https://authenticator.cursor.sh/?client_id=client_01GS6W3C96KW4WRS6Z93JCE2RJ&redirect_uri=https%3A%2F%2Fcursor.com%2Fapi%2Fauth%2Fcallback&response_type=code&state=%257B%2522returnTo%2522%253A%2522%252Fsettings%2522%257D&authorization_session_id={self.session_id}"

            random_hash = generate_random_hash()
            payload = f'["{random_hash}"]'

            headers = {
                "next-action": "a67eb6646e43eddcbd0d038cbee664aac59f5a53",
                "pragma": "no-cache",
                "cache-control": "no-cache",
                "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                "content-type": "text/plain;charset=UTF-8",
            }

            response = self.session.post(
                url=url,
                data=payload,
                headers=headers,
                proxies=self.proxy,
                impersonate="chrome131",
                verify=False
            )

            if response.status_code != 200:
                logger.error(f"{EMOJI['ERROR']} 获取Webkit ID请求失败: HTTP {response.status_code}")
                return None

            # 从响应中提取Webkit ID
            for line in response.text.split('\n'):
                if line.startswith("1:"):
                    try:
                        json_data = json.loads(line.replace("1:", ""))
                        webkit_id = json_data.get("payload")
                        if webkit_id:
                            logger.info(f"{EMOJI['SUCCESS']} 成功获取Webkit ID")
                            # 将Webkit ID添加到Cookie中
                            self.session.cookies.update({"__wuid": webkit_id})
                            return webkit_id
                    except Exception:
                        pass

            logger.error(f"{EMOJI['ERROR']} 未能从响应中提取Webkit ID")
            return None

        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 获取Webkit ID过程中发生错误: {str(e)}")
            return None

    def _build_register_form(self, boundary, token):
        """构建注册表单数据"""
        fields = {
            "1_state": '{"returnTo":"/settings"}',
            "1_redirect_uri": "https://cursor.com/api/auth/callback",
            "1_bot_detection_token": token,
            "1_first_name": self.first_name,
            "1_last_name": self.last_name,
            "1_email": self.email_address,
            "1_password": self.password,
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
        return "\r\n".join(form_data)

    def _extract_auth_token(self, response_text: str) -> str | None:
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
        except Exception as e:
            logger.error(f"提取token失败: {str(e)}")
            # logger.debug("响应内容预览:", response_text[:200])
            pass

        return None

    def _submit_registration(self, token):
        """提交注册表单"""
        try:
            url = "https://authenticator.cursor.sh/sign-up/password"

            boundary = "----WebKitFormBoundaryIpRMVl1c9RMCdEYH"
            form_data = self._build_register_form(boundary, token)

            headers = {
                "accept": "text/x-component",
                "next-action": "770926d8148e29539286d20e1c1548d2aff6c0b9",
                "content-type": f"multipart/form-data; boundary={boundary}",
                "origin": "https://authenticator.cursor.sh",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
            }

            # 如果有WebKit指纹，添加到Cookie
            if self.webkit_id:
                headers["Cookie"] = f"__wuid={self.webkit_id}"
                # logger.debug("已将WebKit指纹添加到callback请求的Cookie")

            params = {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email_address,
                "state": "%7B%22returnTo%22%3A%22%2Fsettings%22%7D",
                "redirect_uri": "https://cursor.com/api/auth/callback",
                "authorization_session_id": self.session_id,
            }

            response = self.session.post(
                url=url,
                params=params,
                data=form_data,
                headers=headers,
                proxies=self.proxy,
                impersonate="chrome131",
                verify=False
            )
            # 提取pending_token
            pending_token = self._extract_auth_token(response.text)
            if pending_token:
                logger.info(f"{EMOJI['SUCCESS']} 成功获取pending token: {pending_token}")
                return pending_token

            # 如果_extract_auth_token提取失败，尝试使用之前的方法
            json_data = extract_json_from_response(response.text)
            if not json_data:
                logger.error(f"{EMOJI['ERROR']} 未能从响应中提取JSON数据")
                return None

            pending_token = json_data.get('payload', {}).get('email', {}).get('token')
            if pending_token:
                logger.info(f"{EMOJI['SUCCESS']} 成功获取pending token")
                return pending_token
            else:
                logger.error(f"{EMOJI['ERROR']} 未能从响应中提取pending token")
                return None

        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 提交注册表单过程中发生错误: {str(e)}")
            return None

    def _build_verify_form(self, boundary, token, code):
        """构建验证邮箱表单数据"""
        fields = {
            "1_pending_authentication_token": self.pending_token,
            "1_email": self.email_address,
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

    def _verify_email(self, token):
        """验证邮箱"""
        try:
            url = "https://authenticator.cursor.sh/email-verification"

            boundary = "----WebKitFormBoundaryAGfPNxpKJZB5YIIP"
            form_data = self._build_verify_form(boundary, token, self.verification_code)

            headers = {
                "accept": "text/x-component",
                "content-type": f"multipart/form-data; boundary={boundary}",
                "next-action": "e75011da58d295bef5aa55740d0758a006468655",
                "origin": "https://authenticator.cursor.sh",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
            }

            # 如果有WebKit指纹，添加到Cookie
            if self.webkit_id:
                headers["Cookie"] = f"__wuid={self.webkit_id}"
                # logger.debug("已将WebKit指纹添加到验证请求的Cookie")

            params = {
                "email": self.email_address,
                "pending_authentication_token": self.pending_token,
                "state": "%7B%22returnTo%22%3A%22%2Fsettings%22%7D",
                "redirect_uri": "https://cursor.com/api/auth/callback",
                "authorization_session_id": self.session_id,
            }

            response = self.session.post(
                url=url,
                params=params,
                data=form_data,
                headers=headers,
                proxies=self.proxy,
                impersonate="chrome131",
                verify=False,
                allow_redirects=False
            )

            # 检查重定向
            redirect_url = response.headers.get('x-action-redirect')
            if redirect_url:
                logger.info(f"{EMOJI['SUCCESS']} 成功获取重定向URL: {redirect_url}")
                return redirect_url

            # 兼容旧版API，也检查Location头
            if response.status_code == 303:
                redirect_url = response.headers.get('Location')
                if redirect_url:
                    logger.info(f"{EMOJI['SUCCESS']} 成功获取重定向URL(从Location): {redirect_url}")
                    return redirect_url

            logger.error(f"{EMOJI['ERROR']} 未能从响应中获取重定向URL: {response.status_code}")
            return None

        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 验证邮箱过程中发生错误: {str(e)}")
            return None

    def _handle_callback(self, redirect_url):
        """处理回调请求，获取cookie"""
        try:
            # 1. 从重定向URL中提取参数
            parsed = urllib.parse.urlparse(redirect_url)
            query_params = urllib.parse.parse_qs(parsed.query)
            code = query_params.get("code", [""])[0]
            if not code:
                logger.error(f"{EMOJI['ERROR']} 未从重定向URL中找到code参数")
                return None

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "zh-CN,zh;q=0.9",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "upgrade-insecure-requests": "1",
            }

            # 如果有WebKit指纹，添加到Cookie
            if self.webkit_id:
                headers["Cookie"] = f"__wuid={self.webkit_id}"
                # logger.debug("已将WebKit指纹添加到callback请求的Cookie")

            callback_url = "https://www.cursor.com/api/auth/callback"
            params = {"code": code, "state": "%7B%22returnTo%22%3A%22%2Fsettings%22%7D"}

            response = self.session.get(
                url=callback_url,
                params=params,
                headers=headers,
                proxies=self.proxy,
                impersonate="chrome131",
                verify=False,
                allow_redirects=False
            )

            # 从Set-Cookie头提取会话cookie
            cookie_header = response.headers.get("set-cookie")
            if cookie_header:
                cookie_value = extract_cookie(cookie_header)
                if cookie_value:
                    logger.info(f"{EMOJI['SUCCESS']} 从响应头部提取会话cookie成功")
                    return cookie_value

            # 检查cookies对象
            cookie_value = response.cookies.get("WorkosCursorSessionToken")
            if cookie_value:
                logger.info(f"{EMOJI['SUCCESS']} 成功获取会话cookie")
                return cookie_value

            logger.error(f"{EMOJI['ERROR']} 未在响应中找到会话cookie")
            return None

        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 处理回调过程中发生错误: {str(e)}")
            return None

    def _get_token(self):
        """获取访问Token"""
        try:
            # 生成随机参数
            random_verifier = generate_code_verifier()
            random_challenge = generate_code_challenge(random_verifier)
            random_uuid = str(uuid.uuid4())

            # 设置请求头和cookies
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
            }

            # 设置cookies
            self.session.cookies.update({
                "NEXT_LOCALE": "cn",
                "WorkosCursorSessionToken": self.cookie,
            })

            # 初始化验证过程
            url = "https://www.cursor.com/api/auth/loginDeepCallbackControl"
            data = {
                "uuid": random_uuid,
                "challenge": random_challenge,
            }

            # 发送请求初始化验证过程
            response = self.session.post(
                url=url,
                json=data,
                headers=headers,
                proxies=self.proxy,
                impersonate="chrome131",
                verify=False
            )

            logger.info(f"{EMOJI['KEY']} 开始获取token...")

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
                    logger.info(f"{EMOJI['WAIT']} 正在轮询获取token... (尝试 {attempt + 1}/{max_attempts})")

                    poll_response = self.session.get(
                        url=poll_url,
                        headers=poll_headers,
                        proxies=self.proxy,
                        impersonate="chrome131",
                        verify=False
                    )

                    # 直接尝试解析响应体，不依赖状态码
                    try:
                        response_text = poll_response.text
                        response_data = json.loads(response_text)

                        if "accessToken" in response_data:
                            access_token = response_data.get("accessToken")
                            refresh_token = response_data.get("refreshToken", access_token)
                            auth_id = response_data.get("authId")

                            if access_token and auth_id:
                                # 从authId中提取user_id部分
                                user_id = auth_id.split("|")[1]
                                # 构建cursor_cookie格式 (确保使用%3A%3A而不是::)
                                full_cookie = f"{user_id}%3A%3A{access_token}"

                                # 尝试刷新token以确保有效性
                                processed_token = process_token(full_cookie, self.proxy is not None)

                                # 如果返回的token和原始token不同，则使用新token
                                if processed_token != access_token:
                                    logger.info(f"{EMOJI['SUCCESS']} 成功刷新token")
                                    access_token = processed_token
                                    # 更新full_cookie
                                    full_cookie = f"{user_id}%3A%3A{access_token}"

                                # 确保与刷新cursor程序兼容的token格式
                                logger.info(f"{EMOJI['SUCCESS']} 成功获取并处理访问token")
                                return {
                                    "access_token": access_token,
                                    "refresh_token": refresh_token,
                                    "full_cookie": full_cookie,
                                }
                            else:
                                logger.info(f"{EMOJI['WAIT']} 获取到访问令牌但缺少authId，继续尝试...")
                                continue
                        else:
                            logger.info(f"{EMOJI['WAIT']} 等待token生成...")

                    except json.JSONDecodeError:
                        logger.error(f"{EMOJI['ERROR']} 解析响应JSON失败")
                    except Exception as e:
                        logger.error(f"{EMOJI['ERROR']} 解析响应过程发生异常: {str(e)}")

                except Exception as e:
                    logger.error(f"{EMOJI['ERROR']} 轮询请求过程发生异常: {str(e)}")

                # 等待再次尝试
                time.sleep(retry_interval)

            logger.error(f"{EMOJI['ERROR']} 获取token超时，达到最大尝试次数")
            return None

        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 获取token过程中发生错误: {str(e)}")
            return None


def register_cursor(
        email_api_type='tempmail.lol',
        email_api_key=None,
        captcha_api_type='ez-captcha',
        captcha_api_key=None,
        proxy=None,
        use_mock=False
):
    """
    快速注册Cursor账号的便捷函数
    
    参数:
        email_api_type: 邮箱API类型，支持'mail.td'、'kopeechka'等
        email_api_key: 邮箱API密钥
        captcha_api_type: 验证码API类型，支持'capsolver'、'2captcha'等
        captcha_api_key: 验证码API密钥
        proxy: 代理设置，格式为 "http://user:pass@ip:port" 或 {"http": "...", "https": "..."}
        use_mock: 是否使用模拟模式（用于测试）
        
    返回:
        dict: 注册结果
    """
    try:
        # 创建注册客户端
        client = CursorRegister(
            email_api_type=email_api_type,
            email_api_key=email_api_key,
            captcha_api_type=captcha_api_type,
            captcha_api_key=captcha_api_key,
            proxy=proxy,
            use_mock=use_mock
        )

        # 执行注册流程
        result = client.register()
        return result

    except Exception as e:
        logger.error(f"{EMOJI['ERROR']} 注册过程中发生未处理的错误: {str(e)}")
        return {
            "success": False,
            "message": f"注册过程中发生未处理的错误: {str(e)}"
        }
