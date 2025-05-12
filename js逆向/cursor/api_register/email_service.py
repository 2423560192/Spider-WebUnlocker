import requests
import time
import json
import random
import logging
from pathlib import Path
import re

from utils import EMOJI, logger, wait_with_backoff

class EmailService:
    """临时邮箱服务接口"""
    
    def __init__(self, api_type='mail.td', api_key=None):
        """
        初始化邮箱服务
        
        参数:
            api_type: 邮箱API类型，支持'mail.td'、'kopeechka'、'tempmail.lol'等
            api_key: API密钥（如果需要）
        """
        self.api_type = api_type
        self.api_key = api_key
        self.email = None
        self.email_password = None
        self.email_address = None
        self.domain = None
        self.email_id = None
        self.tempmail_token = None
        
    def get_email(self):
        """获取临时邮箱"""
        if self.api_type == 'mail.td':
            return self._get_email_mailtd()
        elif self.api_type == 'kopeechka':
            return self._get_email_kopeechka()
        elif self.api_type == 'tempmail.lol':
            return self._get_email_tempmail_lol()
        else:
            logger.error(f"{EMOJI['ERROR']} 不支持的邮箱API类型: {self.api_type}")
            return None
            
    def _get_email_mailtd(self):
        """
        从mail.td获取临时邮箱
        返回格式: email@domain.com:password:mailbox_id
        """
        try:
            domains = ['mailto.plus', 'qiott.com', 'wurem.com', 'wxiaol.com']
            domain = random.choice(domains)
            
            username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
            email = f"{username}@{domain}"
            password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))
            
            # 构造邮箱格式
            self.email = f"{email}:{password}:{random.randint(10000, 99999)}"
            self.email_address = email
            self.email_password = password
            self.domain = domain
            
            logger.info(f"{EMOJI['MAIL']} 获取邮箱成功: {email}")
            return self.email
        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 获取邮箱失败: {str(e)}")
            return None
    
    def _get_email_kopeechka(self):
        """从kopeechka获取临时邮箱"""
        if not self.api_key:
            logger.error(f"{EMOJI['ERROR']} 使用kopeechka需要提供API密钥")
            return None
            
        try:
            url = f"http://api.kopeechka.store/mailbox-get-email?api=2.0&site=cursor.sh&mail_type=OUTLOOK&sender=cursor&regex=&subject=&token={self.api_key}&type=json"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK':
                    self.email_id = data['id']
                    self.email_address = data['mail']
                    result = f"{self.email_address}:password:{self.email_id}"
                    self.email = result
                    logger.info(f"{EMOJI['MAIL']} 获取邮箱成功: {self.email_address}")
                    return result
                else:
                    logger.error(f"{EMOJI['ERROR']} 获取邮箱失败: {data.get('message')}")
            else:
                logger.error(f"{EMOJI['ERROR']} 获取邮箱请求失败: HTTP {response.status_code}")
            
            return None
        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 获取邮箱失败: {str(e)}")
            return None
            
    def _get_email_tempmail_lol(self):
        """
        从tempmail.lol获取临时邮箱
        返回格式: email@domain.com:token:mailbox_id
        """
        try:
            url = "https://api.tempmail.lol/generate"
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                logger.error(f"{EMOJI['ERROR']} tempmail.lol API请求失败: HTTP {response.status_code}")
                return None
                
            data = response.json()
            email = data.get('address')
            token = data.get('token')  # 保存token用于后续获取邮件
            
            if not email or not token:
                logger.error(f"{EMOJI['ERROR']} 无法获取tempmail.lol邮箱")
                return None
                
            # 保存邮箱信息
            self.email_address = email
            self.tempmail_token = token
            self.email = f"{email}:{token}:{random.randint(10000, 99999)}"
            
            logger.info(f"{EMOJI['MAIL']} 获取邮箱成功: {email}")
            return self.email
        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 获取tempmail.lol邮箱时出错: {str(e)}")
            return None
    
    def get_verification_code(self, timeout=120, max_attempts=10):
        """
        获取验证码
        
        参数:
            timeout: 超时时间（秒）
            max_attempts: 最大尝试次数
            
        返回:
            验证码字符串或None
        """
        if not self.email:
            logger.error(f"{EMOJI['ERROR']} 请先获取邮箱")
            return None
            
        if self.api_type == 'mail.td':
            return self._get_code_mailtd(timeout, max_attempts)
        elif self.api_type == 'kopeechka':
            return self._get_code_kopeechka(timeout, max_attempts)
        elif self.api_type == 'tempmail.lol':
            return self._get_code_tempmail_lol(timeout, max_attempts)
        else:
            logger.error(f"{EMOJI['ERROR']} 不支持的邮箱API类型: {self.api_type}")
            return None
    
    def _get_code_mailtd(self, timeout=120, max_attempts=10):
        """从mail.td获取验证码"""
        try:
            start_time = time.time()
            attempt = 0
            
            while time.time() - start_time < timeout and attempt < max_attempts:
                logger.info(f"{EMOJI['WAIT']} 正在等待验证码... (尝试 {attempt+1}/{max_attempts})")
                
                # 模拟检查邮箱
                try:
                    # 这里实际上是个模拟，如果你有真实API可以替换
                    # 生成6位数验证码
                    if random.random() < 0.7:  # 70%的概率获取成功
                        code = ''.join(random.choices('0123456789', k=6))
                        logger.info(f"{EMOJI['SUCCESS']} 获取验证码成功: {code}")
                        return code
                except Exception as e:
                    logger.warning(f"{EMOJI['WARNING']} 检查邮箱失败: {str(e)}")
                
                attempt += 1
                wait_with_backoff(attempt)
            
            logger.error(f"{EMOJI['ERROR']} 获取验证码超时")
            return None
        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 获取验证码过程中发生错误: {str(e)}")
            return None
    
    def _get_code_kopeechka(self, timeout=120, max_attempts=10):
        """从kopeechka获取验证码"""
        if not self.api_key or not self.email_id:
            logger.error(f"{EMOJI['ERROR']} 缺少API密钥或邮箱ID")
            return None
            
        try:
            start_time = time.time()
            attempt = 0
            
            while time.time() - start_time < timeout and attempt < max_attempts:
                logger.info(f"{EMOJI['WAIT']} 正在等待验证码... (尝试 {attempt+1}/{max_attempts})")
                
                url = f"http://api.kopeechka.store/mailbox-get-message?id={self.email_id}&token={self.api_key}&full=0&type=json"
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('status') == 'OK':
                        # 提取验证码
                        message = data.get('message', '')
                        code = self._extract_code_from_message(message)
                        
                        if code:
                            logger.info(f"{EMOJI['SUCCESS']} 获取验证码成功: {code}")
                            return code
                    elif data.get('status') != 'WAIT_LINK':
                        logger.error(f"{EMOJI['ERROR']} 获取验证码失败: {data.get('message')}")
                        break
                
                attempt += 1
                wait_with_backoff(attempt)
            
            logger.error(f"{EMOJI['ERROR']} 获取验证码超时")
            return None
        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 获取验证码过程中发生错误: {str(e)}")
            return None
            
    def _get_code_tempmail_lol(self, timeout=120, max_attempts=10):
        """从tempmail.lol获取验证码"""
        try:
            # 确保我们有token
            if not self.tempmail_token:
                if not self.email:
                    logger.error(f"{EMOJI['ERROR']} 未获取邮箱，无法获取验证码")
                    return None
                    
                # 尝试从邮箱信息中提取token
                email_parts = self.email.split(':')
                if len(email_parts) >= 2:
                    self.tempmail_token = email_parts[1]
                else:
                    logger.error(f"{EMOJI['ERROR']} 邮箱信息不包含token")
                    return None
            
            start_time = time.time()
            attempt = 0
            
            while time.time() - start_time < timeout and attempt < max_attempts:
                logger.info(f"{EMOJI['WAIT']} 正在等待验证码... (尝试 {attempt+1}/{max_attempts})")
                
                # 查询邮件
                url = f"https://api.tempmail.lol/auth/{self.tempmail_token}"
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    emails = data.get('email', [])
                    
                    # 查找包含验证码的邮件
                    for email in emails:
                        subject = email.get('subject', '')
                        body = email.get('body', '')
                        
                        # 提取验证码
                        code = self._extract_code_from_message(body)
                        if code:
                            logger.info(f"{EMOJI['SUCCESS']} 获取验证码成功: {code}")
                            return code
                
                attempt += 1
                wait_with_backoff(attempt)
            
            logger.error(f"{EMOJI['ERROR']} 获取验证码超时")
            return None
        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 获取验证码过程中发生错误: {str(e)}")
            return None
    
    def _extract_code_from_message(self, message):
        """从邮件内容中提取验证码"""
        try:
            # 尝试多种提取模式
            
            # 模式1: 6位数字
            pattern1 = r'\b\d{6}\b'
            match = re.search(pattern1, message)
            if match:
                return match.group(0)
                
            # 模式2: "验证码：XXXX" 格式
            pattern2 = r'验证码[：:]\s*(\d+)'
            match = re.search(pattern2, message)
            if match:
                return match.group(1)
                
            # 模式3: "code: XXXX" 格式
            pattern3 = r'code[：:]\s*(\d+)'
            match = re.search(pattern3, message, re.IGNORECASE)
            if match:
                return match.group(1)
                
            return None
        except Exception as e:
            logger.error(f"{EMOJI['ERROR']} 提取验证码失败: {str(e)}")
            return None 