import logging
import os
import sys
import json
from logging.handlers import RotatingFileHandler

# 日志级别映射
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# 创建日志目录
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 统一的日志格式
CONSOLE_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
FILE_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'

# 加载日志配置
def load_log_config():
    """
    从配置文件加载日志配置
    
    Returns:
        dict: 日志配置字典
    """
    config_file = '../conf/log_config.json'
    default_config = {
        "console_level": "info",
        "file_level": "info",
        "log_file": "linkedin.log",
        "max_file_size": 5*1024*1024,  # 5MB
        "backup_count": 3,
        "module_levels": {
            "__main__": "info",
            "thread_pool": "info",
            "proxy": "info",
            "linkedin_unlocker": "info",
            "batch_login": "info",
            "captcha_solver": "info"
        },
        "debug_modules": []
    }
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置和加载的配置
                for key, value in config.items():
                    default_config[key] = value
    except Exception as e:
        print(f"加载日志配置文件出错: {str(e)}，将使用默认配置")
    
    return default_config

# 配置根日志
def configure_root_logger():
    """
    配置根日志器，从配置文件加载设置
    
    Returns:
        logging.Logger: 配置好的根日志器
    """
    # 加载配置
    config = load_log_config()
    
    console_level = config["console_level"]
    file_level = config["file_level"]
    log_file = config["log_file"]
    max_size = config["max_file_size"]
    backup_count = config["backup_count"]
    
    root_logger = logging.getLogger()
    
    # 清除已有的处理器
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
    # 设置根日志级别为最低级别
    root_logger.setLevel(logging.DEBUG)  
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVELS.get(console_level, logging.INFO))
    console_handler.setFormatter(logging.Formatter(CONSOLE_FORMAT))
    root_logger.addHandler(console_handler)
    
    # 文件处理器 (使用RotatingFileHandler进行日志轮转)
    file_path = os.path.join(LOG_DIR, log_file)
    file_handler = RotatingFileHandler(
        file_path,
        maxBytes=max_size, 
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(LOG_LEVELS.get(file_level, logging.INFO))
    file_handler.setFormatter(logging.Formatter(FILE_FORMAT))
    root_logger.addHandler(file_handler)
    
    return root_logger

# 获取模块日志器
def get_logger(name):
    """
    获取模块的日志器，根据配置设置日志级别
    
    Args:
        name: 模块名称
        
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 加载配置
    config = load_log_config()
    module_levels = config.get("module_levels", {})
    debug_modules = config.get("debug_modules", [])
    
    # 确定模块日志级别
    module_name = name.split('.')[-1]  # 取最后一部分作为模块名
    
    # 调试模式优先
    if module_name in debug_modules:
        level = 'debug'
    else:
        level = module_levels.get(module_name, 'info')
    
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(level, logging.INFO))
    
    # 不添加处理器，使用根日志器的处理器
    logger.propagate = True
    
    return logger

# 初始化根日志器
configure_root_logger() 