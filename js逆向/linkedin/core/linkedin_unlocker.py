import requests
from bs4 import BeautifulSoup
import json
import os
import threading
from captcha.captcha_solver import CaptchaSolver
from utils.proxy import ProxyManager
from utils.logger_config import get_logger

# 获取模块日志器
logger = get_logger(__name__)


class LinkedInUnlocker:
    """
    LinkedIn 解锁器类，用于处理登录过程
    """

    def __init__(self, random_ua, username, password):
        """初始化解锁器"""

        # 代理ip
        self.proxy_manager = ProxyManager()
        self.proxy_manager.get_new_proxy()
        self.proxy = self.proxy_manager.get_proxy_dict()
        self.random_ua = random_ua
        logger.info(f"🌐 当前使用代理IP: {self.proxy}")
        logger.info(f"🌐 当前使用UA: {self.random_ua}")

        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': random_ua,
        })
        # 默认账号信息
        self.username = ""
        self.password = ""

        # 实例化验证码解析器
        self.captcha_solver = CaptchaSolver(self.session, self.proxy)

        # 状态追踪
        self.is_logged_in = False
        self.error_message = None
        self.max_retry_count = 3
        self.retry_delay = 5

        self.username = username
        self.password = password

        self.load_config()

    def load_config(self):
        """
        加载配置文件，包含用户名和密码

        Returns:
            bool: 配置加载是否成功
        """
        config_file = 'conf/config.json'
        try:
            # 检查配置文件是否存在
            if not os.path.exists(config_file):
                logger.warning(f"⚠️ 配置文件 {config_file} 不存在，将使用默认设置")
                return False

            # 读取配置文件
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 更新User-Agent
            if 'user_agent' in config and config['user_agent']:
                self.session.headers.update({
                    'user-agent': config['user_agent']
                })
                logger.info(f"✅ 已加载User-Agent: {config['user_agent']}")

            return bool(self.username and self.password)

        except json.JSONDecodeError:
            logger.error(f"❌ 配置文件 {config_file} JSON格式错误")
            return False
        except Exception as e:
            logger.error(f"❌ 加载配置文件时出错: {str(e)}")
            return False

    def login(self):
        """
        执行登录过程
        
        Returns:
            最后一次登录响应
        """
        if not self.username or not self.password:
            logger.error("❌ 用户名或密码为空，请检查配置文件")
            self.error_message = "用户名或密码为空，请检查配置文件"
            return False

        logger.info(f"🔑 开始登录LinkedIn，用户名: {self.username}")

        # 添加重试机制
        retry_count = 0

        while retry_count < self.max_retry_count:
            try:
                # 访问登录页面获取CSRF令牌和其他表单参数
                login_page_url = 'https://www.linkedin.com/checkpoint/rm/sign-in-another-account'
                logger.info(f"请求登录页面: {login_page_url}")

                login_page_response = self.session.get(
                    login_page_url,
                    proxies=self.proxy,
                    timeout=20  # 设置较长的超时时间
                )

                if login_page_response.status_code >= 400:
                    logger.warning(f"登录页面请求失败，状态码: {login_page_response.status_code}")
                    raise requests.exceptions.RequestException(f"登录页面请求失败: {login_page_response.status_code}")

                login_soup = BeautifulSoup(login_page_response.text, 'html.parser')

                # 提取登录表单参数
                form_data = self.extract_form_data(login_soup)

                if not form_data:
                    logger.error("❌ 无法提取登录表单数据")
                    raise ValueError("无法提取登录表单数据")

                form_data['session_key'] = self.username
                form_data['session_password'] = self.password

                # 提交登录请求
                login_submit_url = 'https://www.linkedin.com/checkpoint/lg/login-submit'
                logger.info(f"提交登录请求: {login_submit_url}")

                login_response = self.session.post(
                    login_submit_url,
                    data=form_data,
                    allow_redirects=True,
                    proxies=self.proxy,
                    timeout=30  # 设置较长的超时时间
                )

                logger.info(f"🌐 登录后重定向URL: {login_response.url}")
                logger.info(f"📊 登录响应状态码: {login_response.status_code}")

                # # 保存登录的页面
                # with open('login.html', 'w', encoding='utf-8') as f:
                #     f.write(login_response.text)

                # 检查是否登录成功
                if 'feed' in login_response.url or 'mynetwork' in login_response.url:
                    logger.info("✅ 登录成功，已进入LinkedIn主页")
                    return login_response

                # 获取是否有安全验证
                soup = BeautifulSoup(login_response.text, 'html.parser')

                # 查找<h1>标签
                h1_tag = soup.find('h1')

                # 提取<h1>标签中的文本
                if h1_tag and h1_tag.text == '进行快速安全验证':
                    # 检查是否需要进一步验证
                    if 'checkpoint' in login_response.url:
                        logger.info(f"🔒 登录需要进一步验证: {login_response.url}")
                        verification_result = self.handle_verification(login_response.url)

                        # 如果验证结果是Response对象，返回该响应
                        if isinstance(verification_result, requests.Response):
                            return verification_result

                        # 如果验证成功但没有返回Response对象，返回原始登录响应
                        if verification_result:
                            return login_response

                # 默认返回登录响应，无论成功与否
                return login_response

            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout,
                    requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                # 代理相关错误，尝试切换代理
                retry_count += 1
                logger.warning(f"代理连接错误: {str(e)}, 尝试切换代理 (尝试 {retry_count}/{self.max_retry_count})")

                # 切换代理
                new_proxy = self.proxy_manager.switch_proxy()
                if new_proxy:
                    self.proxy = self.proxy_manager.get_proxy_dict()
                    # 更新验证码解析器的代理
                    self.captcha_solver.proxy = self.proxy
                    logger.info(f"已切换到新代理: {self.proxy}")
                else:
                    logger.error("无法获取新的代理IP")

                # 指数退避延迟，使用Event而非sleep
                wait_time = self.retry_delay * (2 ** (retry_count - 1))
                logger.info(f"等待 {wait_time} 秒后重试...")
                wait_event = threading.Event()
                wait_event.wait(wait_time)

            except Exception as e:
                # 其他错误
                retry_count += 1
                logger.error(f"登录过程中出错: {str(e)}")

                if retry_count < self.max_retry_count:
                    wait_time = self.retry_delay * (2 ** (retry_count - 1))
                    logger.info(f"等待 {wait_time} 秒后重试... ({retry_count}/{self.max_retry_count})")
                    wait_event = threading.Event()
                    wait_event.wait(wait_time)
                else:
                    logger.error(f"登录失败，已达到最大重试次数 {self.max_retry_count}")
                    raise

        # 如果所有重试都失败，返回False
        logger.error("所有登录尝试均失败")
        return False

    def extract_form_data(self, soup):
        """
        从登录页面提取表单数据
        
        Args:
            soup: BeautifulSoup 对象
            
        Returns:
            表单数据字典
        """
        form = soup.find('form', {'class': 'login__form'})
        if not form:
            return None

        form_data = {}
        for input_tag in form.find_all('input'):
            name = input_tag.get('name')
            value = input_tag.get('value', '')
            if name:
                form_data[name] = value

        return form_data

    def handle_verification(self, verification_url):
        """
        处理验证页面
        
        Args:
            verification_url: 验证页面URL
            
        Returns:
            是否验证成功
        """
        logger.info(f"🔒 处理验证页面: {verification_url}")

        # 使用验证码解析器解决验证挑战
        verification_result = self.captcha_solver.solve(verification_url)


        redirect_url = verification_result.url
        logger.info(f"🔄 重定向URL: {redirect_url}")

        # 检查原始重定向是否已经表明登录成功
        if 'feed' in redirect_url or 'mynetwork' in redirect_url:
            logger.info("✅ 验证成功，已登录到LinkedIn主页")

        return verification_result
