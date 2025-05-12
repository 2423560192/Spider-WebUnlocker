"""
配置文件加载模块
"""
import configparser
from pathlib import Path

def load_config():
    """从配置文件加载配置项
    
    Returns:
        configparser.ConfigParser: 配置对象
    """
    config = configparser.ConfigParser()
    # 使用绝对路径确保可以正确找到配置文件
    root_dir = Path(__file__).parent.parent
    config_path = root_dir / 'conf' / 'conf.ini'
    
    if config_path.exists():
        try:
            # 使用UTF-8编码读取配置文件
            config.read(config_path, encoding='utf-8')
        except Exception as e:
            print(f"读取配置文件错误: {str(e)}")
    
    return config

def get_api_keys():
    """获取API密钥配置
    
    Returns:
        tuple: (email_api_key, captcha_api_key)
    """
    config = load_config()
    
    # 默认值
    default_email_key = ""
    default_captcha_key = ""
    
    if 'api_keys' in config:
        return (
            config['api_keys'].get('email_api_key', default_email_key),
            config['api_keys'].get('captcha_api_key', default_captcha_key)
        )
    
    return default_email_key, default_captcha_key

def save_config(config):
    """保存配置到文件
    
    Args:
        config (configparser.ConfigParser): 配置对象
    
    Returns:
        bool: 是否保存成功
    """
    try:
        root_dir = Path(__file__).parent.parent
        config_path = root_dir / 'conf' / 'conf.ini'
        # 使用UTF-8编码保存配置文件
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)
        return True
    except Exception as e:
        print(f"保存配置文件错误: {str(e)}")
        return False 