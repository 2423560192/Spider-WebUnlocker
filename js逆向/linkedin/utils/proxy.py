import requests
import json
import time
import os
import threading
import re
from utils.logger_config import get_logger

# 获取模块日志器
logger = get_logger(__name__)


class ProxyManager:
    """
    代理IP管理器，用于获取和管理代理IP
    """

    def __init__(self, api_url=None):
        """
        初始化代理管理器

        Args:
            api_url: 代理API的URL
        """
        # 如果未提供参数，尝试从配置文件加载
        config = self.load_config()

        # 优先使用传入的参数，如果没有则使用配置文件中的值，最后使用默认值
        self.api_url = api_url or config.get('proxy_api_url') or "http://api.your-proxy-provider.com/get-ip"

        self.current_proxy = None
        self.last_fetch_time = 0
        self.min_fetch_interval = 5  # 最小获取间隔（秒）
        self.max_retry_count = 3  # 获取代理的最大重试次数
        self.proxy_cache = []  # 缓存已获取的代理
        self.max_cache_size = 5  # 最大缓存代理数量
        self.lock = threading.Lock()  # 添加线程锁以保护共享资源
        logger.info(f"代理管理器初始化完成，API URL: {self.api_url}")

    def load_config(self):
        """从配置文件加载代理API配置信息"""
        config_file = 'conf/config.json'
        config = {}
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info("已从配置文件加载代理设置")
            else:
                logger.warning(f"配置文件 {config_file} 不存在，将使用默认设置")
        except json.JSONDecodeError:
            logger.error(f"配置文件 {config_file} JSON格式错误")
        except Exception as e:
            logger.error(f"加载配置文件时出错: {str(e)}")
        return config

    def get_new_proxy(self, force_new=False):
        """
        从API获取新的代理IP

        Args:
            force_new: 是否强制获取新代理，忽略缓存

        Returns:
            dict: 包含代理信息的字典，如果获取失败则返回None
        """
        # 如果有缓存代理且不强制获取新代理，则从缓存中选择
        with self.lock:
            if not force_new and self.proxy_cache:
                self.current_proxy = self.proxy_cache.pop(0)
                logger.info(f"使用缓存代理: {self.current_proxy['ip']}:{self.current_proxy['port']}")
                return self.current_proxy

        retry_count = 0
        while retry_count < self.max_retry_count:
            try:
                # 检查获取间隔
                current_time = time.time()
                time_since_last = current_time - self.last_fetch_time
                if time_since_last < self.min_fetch_interval:
                    wait_time = self.min_fetch_interval - time_since_last
                    logger.warning(f"代理请求过于频繁，等待 {wait_time:.2f} 秒")
                    # 使用Event替代sleep
                    wait_event = threading.Event()
                    wait_event.wait(wait_time)

                # 发送请求获取代理IP
                logger.info("正在从API获取新的代理IP...")
                response = requests.get(self.api_url, timeout=10)
                self.last_fetch_time = time.time()

                # 检查响应状态
                if response.status_code == 200:
                    # 处理返回的文本格式IP
                    proxy_text = response.text.strip()
                    
                    # 提取IP和端口
                    # 假设返回格式为 "ip:port" 或者包含IP:端口格式的文本
                    ip_port_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)'
                    matches = re.findall(ip_port_pattern, proxy_text)
                    
                    if not matches:
                        logger.warning(f"无法从响应中提取代理IP，响应内容: {proxy_text}")
                        retry_count += 1
                        # 使用Event替代sleep
                        wait_event = threading.Event()
                        wait_event.wait(2)
                        continue
                    
                    # 使用找到的所有代理
                    proxy_list = []
                    for ip, port in matches:
                        proxy_list.append({"ip": ip, "port": port})
                    
                    if not proxy_list:
                        logger.warning("API返回成功但无法解析代理IP数据")
                        retry_count += 1
                        # 使用Event替代sleep
                        wait_event = threading.Event()
                        wait_event.wait(2)
                        continue

                    # 处理第一个代理作为当前代理
                    proxy_data = proxy_list[0]
                    proxy_info = self._create_proxy_info(proxy_data)

                    with self.lock:
                        self.current_proxy = proxy_info

                        # 将其余代理添加到缓存
                        for i in range(1, len(proxy_list)):
                            cache_proxy = self._create_proxy_info(proxy_list[i])
                            self.proxy_cache.append(cache_proxy)
                            if len(self.proxy_cache) >= self.max_cache_size:
                                break

                    logger.info(f"成功获取代理IP: {proxy_info['ip']}:{proxy_info['port']}")

                    # 测试当前代理是否有效
                    if self.test_proxy():
                        return self.current_proxy
                    else:
                        logger.warning(f"代理测试失败，尝试下一个代理")
                        # 如果有缓存代理，尝试使用下一个
                        with self.lock:
                            if self.proxy_cache:
                                self.current_proxy = self.proxy_cache.pop(0)
                                if self.test_proxy():
                                    return self.current_proxy

                        # 如果所有代理都不可用，重试获取
                        retry_count += 1
                        continue
                else:
                    logger.error(f"请求代理API失败: HTTP状态码 {response.status_code}")
                    retry_count += 1
                    # 使用Event替代sleep
                    wait_event = threading.Event()
                    wait_event.wait(2)

            except Exception as e:
                logger.error(f"获取代理IP时出错: {str(e)}")
                retry_count += 1
                # 使用Event替代sleep
                wait_event = threading.Event()
                wait_event.wait(2)

        logger.error(f"获取代理IP失败，已重试 {self.max_retry_count} 次")
        return None

    def _create_proxy_info(self, proxy_data):
        """
        从API响应数据创建代理信息字典
        
        Args:
            proxy_data: 包含IP和端口的字典
            
        Returns:
            dict: 代理信息字典
        """
        proxy_info = {
            'ip': proxy_data.get('ip'),
            'port': proxy_data.get('port'),
            'protocol': 'http',  # 默认使用http协议
            'location': 'Unknown'  # 直接返回的IP格式不包含位置信息
        }

        # 构建代理字符串
        proxy_str = f"{proxy_info['protocol']}://{proxy_info['ip']}:{proxy_info['port']}"
        proxy_info['proxy_str'] = proxy_str

        return proxy_info

    def get_proxy_dict(self):
        """
        获取当前代理的字典格式

        Returns:
            dict: 包含http和https协议的代理字典，适用于requests库
        """
        if not self.current_proxy:
            logger.warning("尝试获取代理字典，但当前没有可用代理")
            return None

        proxy_str = self.current_proxy['proxy_str']
        logger.debug(f"返回代理字典: {proxy_str}")
        return {
            'http': proxy_str,
            'https': proxy_str
        }

    def test_proxy(self, test_url="https://www.linkedin.com", timeout=5):
        """
        测试当前代理是否可用

        Args:
            test_url: 用于测试的URL
            timeout: 连接超时时间（秒）

        Returns:
            bool: 代理是否可用
        """
        if not self.current_proxy:
            logger.warning("没有可测试的代理IP")
            return False

        try:
            proxies = self.get_proxy_dict()
            logger.info(f"测试代理 {self.current_proxy['ip']}:{self.current_proxy['port']}...")

            # 设置较短的超时时间进行测试
            response = requests.get(
                test_url,
                proxies=proxies,
                timeout=timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
            )

            if response.status_code < 400:
                logger.info(f"代理测试成功，状态码: {response.status_code}")
                return True
            else:
                logger.warning(f"代理测试失败，状态码: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"代理测试出错: {str(e)}")
            return False

    def switch_proxy(self):
        """
        切换到新的代理IP
        
        Returns:
            dict: 新的代理信息，如果获取失败则返回None
        """
        logger.info("尝试切换到新的代理IP")

        # 首先尝试从缓存中获取
        with self.lock:
            if self.proxy_cache:
                self.current_proxy = self.proxy_cache.pop(0)
                logger.info(f"从缓存切换到代理: {self.current_proxy['ip']}:{self.current_proxy['port']}")

                # 测试切换的代理
                if self.test_proxy():
                    return self.current_proxy
                else:
                    logger.warning("缓存代理测试失败，尝试获取新代理")

        # 如果缓存为空或测试失败，获取新代理
        return self.get_new_proxy(force_new=True)

# 单例模式，方便全局使用
# proxy_manager = ProxyManager()

# if __name__ == "__main__":
#     proxy_manager.get_new_proxy()
#     # 测试代码
#     print(proxy_manager.get_proxy_dict())
