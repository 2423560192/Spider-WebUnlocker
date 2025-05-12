"""
代理管理模块 - 负责获取和管理代理
"""

import sys
import json
import logging
import requests
import re
from pathlib import Path

# 设置日志
logger = logging.getLogger(__name__)

# 添加项目根路径到sys.path
sys.path.append(str(Path(__file__).parent.parent))
from conf.config_loader import load_config

class ProxyManager:
    """代理管理类，用于获取和管理代理"""
    
    def __init__(self):
        """初始化代理管理器"""
        self.config = load_config()
        self.proxy_enabled = self._get_config_bool('proxy', 'enabled', False)
        self.proxy_api_url = self._get_config('proxy', 'api_url', '')
        self.static_proxy = self._get_config('proxy', 'static_proxy', '')
        self.current_proxy = None
    
    def _get_config(self, section, key, default=None):
        """获取配置项"""
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return default
    
    def _get_config_bool(self, section, key, default=False):
        """获取布尔类型配置项"""
        value = self._get_config(section, key, str(default))
        return value.lower() in ('true', 'yes', '1', 'on')
    
    def get_proxy(self, force_refresh=False):
        """
        获取代理配置
        
        Args:
            force_refresh: 是否强制刷新代理
            
        Returns:
            dict or None: 代理配置字典或None（不使用代理）
        """
        # 如果代理未启用，直接返回None
        if not self.proxy_enabled:
            logger.info("代理功能未启用")
            return None
            
        # 如果有静态代理且不强制刷新，直接返回静态代理
        if self.static_proxy and not force_refresh:
            proxy_dict = {
                "http": self.static_proxy,
                "https": self.static_proxy
            }
            logger.info(f"使用静态代理: {self.static_proxy}")
            self.current_proxy = proxy_dict
            return proxy_dict
            
        # 如果有API URL，尝试获取代理
        if self.proxy_api_url:
            try:
                response = requests.get(self.proxy_api_url, timeout=10)
                if response.status_code == 200:
                    # 解析响应内容
                    proxy_info = self._parse_proxy_response(response.text)
                    if proxy_info:
                        logger.info(f"成功从API获取代理: {proxy_info}")
                        self.current_proxy = proxy_info
                        return proxy_info
                    else:
                        logger.warning(f"代理API返回无效数据: {response.text[:100]}")
                else:
                    logger.error(f"代理API请求失败，状态码: {response.status_code}")
            except Exception as e:
                logger.error(f"获取代理出错: {str(e)}")
                
        # 如果有静态代理作为备选
        if self.static_proxy:
            proxy_dict = {
                "http": self.static_proxy,
                "https": self.static_proxy
            }
            logger.info(f"使用备选静态代理: {self.static_proxy}")
            self.current_proxy = proxy_dict
            return proxy_dict
            
        logger.warning("无法获取有效代理")
        return None
        
    def _parse_proxy_response(self, response_text):
        """
        解析代理API响应
        
        Args:
            response_text: API响应文本
            
        Returns:
            dict or None: 解析后的代理配置或None
        """
        try:
            # 尝试解析JSON响应
            if response_text.strip().startswith('{'):
                data = json.loads(response_text)
                # 检查旋转木马代理API响应格式
                if 'status' in data:
                    # 检查是否成功
                    if data['status'] != 200:
                        logger.error(f"代理API返回错误: {data.get('info', '未知错误')}")
                        return None
                    # 提取代理信息
                    if 'domain' in data and 'port' in data:
                        proxy_str = f"http://{data['domain']}:{data['port']}"
                        return {
                            "http": proxy_str,
                            "https": proxy_str
                        }
                
            # 尝试匹配IP:PORT格式
            ip_port_pattern = r'(\d+\.\d+\.\d+\.\d+):(\d+)'
            match = re.search(ip_port_pattern, response_text)
            if match:
                ip, port = match.groups()
                proxy_str = f"http://{ip}:{port}"
                return {
                    "http": proxy_str,
                    "https": proxy_str
                }
                
            logger.warning(f"无法解析代理响应: {response_text[:100]}")
            return None
        except Exception as e:
            logger.error(f"解析代理响应出错: {str(e)}")
            return None
            
    def test_proxy(self, proxy=None):
        """
        测试代理是否可用
        
        Args:
            proxy: 要测试的代理配置，默认使用当前代理
            
        Returns:
            bool: 代理是否可用
        """
        if proxy is None:
            proxy = self.current_proxy
            
        if not proxy:
            logger.warning("没有可测试的代理")
            return False
            
        try:
            # 用百度测试代理
            test_url = "https://www.baidu.com"
            response = requests.get(test_url, proxies=proxy, timeout=10)
            if response.status_code == 200:
                logger.info("代理测试成功")
                return True
            else:
                logger.warning(f"代理测试失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"代理测试异常: {str(e)}")
            return False

# 单例模式，提供全局代理管理器
_proxy_manager = None

def get_proxy_manager():
    """获取代理管理器单例"""
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager

def get_proxy(force_refresh=False):
    """
    获取代理配置的便捷函数
    
    Args:
        force_refresh: 是否强制刷新代理
        
    Returns:
        dict or None: 代理配置
    """
    manager = get_proxy_manager()
    return manager.get_proxy(force_refresh)

# 测试代码
if __name__ == "__main__":
    # 配置基本日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    # 测试代理获取
    manager = get_proxy_manager()
    proxy = manager.get_proxy()
    
    if proxy:
        print(f"获取到代理: {proxy}")
        # 测试代理
        if manager.test_proxy(proxy):
            print("代理测试成功，可以正常使用")
        else:
            print("代理测试失败，可能无法正常使用")
    else:
        print("未获取到有效代理") 