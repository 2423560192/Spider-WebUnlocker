import requests
import time
import json
import logging
import random
from pathlib import Path

from utils import EMOJI, logger, wait_with_backoff


class CaptchaService:
    """验证码服务接口"""

    def __init__(self, api_type='ez-captcha', api_key=None):
        """
        初始化验证码服务
        
        参数:
            api_type: 验证码API类型，支持'capsolver'、'2captcha'等
            api_key: API密钥
        """
        self.api_type = api_type
        self.api_key = api_key

    def get_turnstile_token(self, site_key='0x4AAAAAAAMNIvC45A4Wjjln', url='https://authenticator.cursor.sh/sign-up',
                            timeout=60):
        """
        获取Turnstile验证码token
        
        参数:
            site_key: Turnstile的site key
            url: 目标URL
            timeout: 超时时间（秒）
            
        返回:
            验证码token或None
        """
        if not self.api_key:
            logger.error(f"{EMOJI['ERROR']} 未提供API密钥")
            return None

        if self.api_type == 'ez-captcha':
            return self._get_token_capsolver(site_key, url, timeout)
        elif self.api_type == '2captcha':
            return self._get_token_2captcha(site_key, url, timeout)
        elif self.api_type == 'mock':
            # 模拟模式，用于测试
            return self._get_token_mock()
        else:
            logger.error(f"{EMOJI['ERROR']} 不支持的验证码API类型: {self.api_type}")
            return None

    def _get_token_capsolver(self, site_key, url, timeout):
        """使用Capsolver获取Turnstile token"""
        try:
            logger.info(f"{EMOJI['INFO']} 正在从Capsolver获取Turnstile token...")

            task_payload = {
                "clientKey": self.api_key,
                "task": {
                    "type": "CloudFlareTurnstileTask",
                    "websiteURL": url,
                    "websiteKey": site_key,
                    "rqData": {
                        "mode": "",
                        "metadataAction": "-sign-up-password",
                        "metadataCdata": ""
                    }
                }
            }

            # 创建任务
            response = requests.post(
                "https://api.ez-captcha.com/createTask",
                json=task_payload,
                timeout=30
            )

            if response.status_code != 200:
                logger.error(f"{EMOJI['ERROR']} ez-Captcha API请求失败: HTTP {response.status_code}")
                return None

            data = response.json()
            if data.get('errorId') > 0:
                logger.error(f"{EMOJI['ERROR']} ez-Captcha错误: {data.get('errorDescription')}")
                return None

            task_id = data.get('taskId')
            if not task_id:
                logger.error(f"{EMOJI['ERROR']} 未能获取ez-Captcha任务ID")
                return None

            # 轮询获取结果
            start_time = time.time()
            while time.time() - start_time < timeout:
                result_payload = {
                    "clientKey": self.api_key,
                    "taskId": task_id
                }

                response = requests.post(
                    "https://api.ez-captcha.com/getTaskResult",
                    json=result_payload,
                    timeout=30
                )

                if response.status_code != 200:
                    logger.error(f"{EMOJI['ERROR']} Capsolver获取结果失败: HTTP {response.status_code}")
                    return None

                data = response.json()
                if data.get('errorId') > 0:
                    logger.error(f"{EMOJI['ERROR']} Capsolver获取结果错误: {data.get('errorDescription')}")
                    return None

                status = data.get('status')
                if status == 'ready':
                    token = data.get('solution', {}).get('token')
                    if token:
                        logger.info(f"{EMOJI['SUCCESS']} 成功获取Turnstile token")
                        return token
                    else:
                        logger.error(f"{EMOJI['ERROR']} Capsolver未返回token")
                        return None

                elif status == 'processing':
                    logger.info(f"{EMOJI['WAIT']} Capsolver正在处理...")
                    time.sleep(3)

                else:
                    logger.error(f"{EMOJI['ERROR']} Capsolver未知状态: {status}")
                    return None

            logger.error(f"{EMOJI['ERROR']} Capsolver处理超时")
            return None

        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} Capsolver处理异常: {str(e)}")
            return None

    def _get_token_2captcha(self, site_key, url, timeout):
        """使用2captcha获取Turnstile token"""
        try:
            logger.info(f"{EMOJI['INFO']} 正在从2captcha获取Turnstile token...")

            # 创建任务
            params = {
                'key': self.api_key,
                'method': 'turnstile',
                'sitekey': site_key,
                'url': url,
                'json': 1
            }

            response = requests.get('https://2captcha.com/in.php', params=params, timeout=30)

            if response.status_code != 200:
                logger.error(f"{EMOJI['ERROR']} 2captcha API请求失败: HTTP {response.status_code}")
                return None

            data = response.json()
            if data.get('status') != 1:
                logger.error(f"{EMOJI['ERROR']} 2captcha错误: {data.get('request')}")
                return None

            request_id = data.get('request')
            if not request_id:
                logger.error(f"{EMOJI['ERROR']} 未能获取2captcha请求ID")
                return None

            # 轮询获取结果
            start_time = time.time()
            while time.time() - start_time < timeout:
                # 等待一段时间再查询结果
                time.sleep(5)

                params = {
                    'key': self.api_key,
                    'action': 'get',
                    'id': request_id,
                    'json': 1
                }

                response = requests.get('https://2captcha.com/res.php', params=params, timeout=30)

                if response.status_code != 200:
                    logger.error(f"{EMOJI['ERROR']} 2captcha获取结果失败: HTTP {response.status_code}")
                    continue

                data = response.json()
                if data.get('status') == 1:
                    token = data.get('request')
                    if token:
                        logger.info(f"{EMOJI['SUCCESS']} 成功获取Turnstile token")
                        return token
                    else:
                        logger.error(f"{EMOJI['ERROR']} 2captcha未返回token")
                        return None

                elif data.get('request') == 'CAPCHA_NOT_READY':
                    logger.info(f"{EMOJI['WAIT']} 2captcha正在处理...")

                else:
                    logger.error(f"{EMOJI['ERROR']} 2captcha错误: {data.get('request')}")
                    return None

            logger.error(f"{EMOJI['ERROR']} 2captcha处理超时")
            return None

        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 2captcha处理异常: {str(e)}")
            return None

    def _get_token_mock(self):
        """模拟获取Turnstile token（用于测试）"""
        logger.info(f"{EMOJI['INFO']} 使用模拟模式获取Turnstile token")
        # 生成一个随机字符串作为token
        mock_token = ''.join(
            random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_') for _ in range(100))
        logger.info(f"{EMOJI['SUCCESS']} 模拟获取Turnstile token成功")
        return mock_token
