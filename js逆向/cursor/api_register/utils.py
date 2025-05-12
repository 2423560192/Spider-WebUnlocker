import base64
import hashlib
import json
import random
import secrets
import string
import time
import uuid
import logging
from pathlib import Path

# 配置日志
log_dir = Path.cwd() / ".cursor_register"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "register_api.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 定义表情符号常量
EMOJI = {
    'START': '🚀',
    'FORM': '📝',
    'VERIFY': '🔄',
    'PASSWORD': '🔑',
    'CODE': '📱',
    'DONE': '✨',
    'ERROR': '❌',
    'WAIT': '⏳',
    'SUCCESS': '✅',
    'MAIL': '📧',
    'KEY': '🔐',
    'UPDATE': '🔄',
    'INFO': 'ℹ️',
    'BROWSER': '🌐',
    'WARNING': '⚠️'
}

def generate_random_password(length=12):
    """生成随机密码"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_name():
    """生成随机姓名"""
    first_names = [
        "James", "John", "Robert", "Michael", "William", "David", "Joseph", "Thomas",
        "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia",
        "Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mason", "Logan", "Alexander"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Anderson", "Wilson", "Taylor", "Thomas", "Moore", "Martin", "Jackson", "Lee",
        "Thompson", "White", "Harris", "Clark", "Lewis", "Walker", "Hall", "Young"
    ]

    # 随机选择姓和名
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    # 修改名字首字母
    new_first_letter = random.choice(string.ascii_uppercase)
    first_name = new_first_letter + first_name[1:]

    return first_name, last_name

def generate_code_verifier():
    """生成随机的32字节数据并进行base64url编码作为code_verifier"""
    random_bytes = secrets.token_bytes(32)
    code_verifier = base64.urlsafe_b64encode(random_bytes).decode("utf-8")
    # 移除填充字符
    code_verifier = code_verifier.rstrip("=")
    return code_verifier

def generate_code_challenge(code_verifier):
    """根据code_verifier计算code_challenge"""
    # 计算SHA256哈希
    sha256_hash = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    # 进行base64url编码
    code_challenge = base64.urlsafe_b64encode(sha256_hash).decode("utf-8")
    # 移除填充字符
    code_challenge = code_challenge.rstrip("=")
    return code_challenge

def extract_cookie(cookie_string):
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
        logger.error(f"{EMOJI['ERROR']} 提取cookie值失败: {str(e)}")
        return cookie_string  # 返回原始字符串作为后备

def generate_random_hash():
    """生成随机哈希值"""
    random_bytes = secrets.token_bytes(16)
    return random_bytes.hex()

def generate_random_uuid():
    """生成随机UUID"""
    return str(uuid.uuid4())


def get_session_user_id():
    """
    获取cookie里面的一个动态值： IndrX2ZuSmZramJSX0NIYUZoRzRzUGZ0cENIVHpHNXk0VE0ya2ZiUkVzQU14X2Fub255bW91c1VzZXJJZCI%3D
    :return:
    """
    input_string = str(uuid.uuid4())

    # 对字符串进行 Base64 编码
    encoded_string = base64.b64encode(input_string.encode('utf-8')).decode('utf-8')
    return encoded_string



def generate_machine_id():
    """生成随机的机器ID"""
    # 生成随机UUID并使用它的哈希作为基础
    new_uuid = str(uuid.uuid4()).upper()
    machine_id_base = hashlib.md5(new_uuid.encode()).hexdigest()
    new_machine_id = f"{machine_id_base[0:8]}-{machine_id_base[8:12]}-{machine_id_base[12:16]}-{machine_id_base[16:20]}-{machine_id_base[20:32]}"
    return new_machine_id

def extract_json_from_response(response_text):
    """从响应文本中提取JSON数据"""
    try:
        # 尝试从特定格式的响应中提取JSON
        for line in response_text.split('\n'):
            if line.startswith('1:'):
                json_str = line[2:]  # 移除 '1:' 前缀
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass

        # 尝试直接解析整个响应
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # 检查是否包含JSON块
        import re
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        match = re.search(json_pattern, response_text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        return None
    except Exception as e:
        logger.error(f"{EMOJI['ERROR']} 提取JSON数据失败: {str(e)}")
        return None

def parse_url_params(url):
    """解析URL参数"""
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return params

def wait_with_backoff(attempt, max_wait=30):
    """指数退避等待"""
    wait_time = min(2 ** attempt, max_wait)
    time.sleep(wait_time)

def save_account_info(email, password, token, refresh_token=None, cookie=None):
    """保存账号信息到文件"""
    try:
        account_file = log_dir / "cursor_accounts.txt"

        with open(account_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"邮箱: {email}\n")
            f.write(f"密码: {password}\n")
            f.write(f"Token: {token}\n")
            if refresh_token:
                f.write(f"Refresh Token: {refresh_token}\n")
            if cookie:
                f.write(f"Cookie: {cookie}\n")
            f.write(f"注册时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n")

        logger.info(f"{EMOJI['SUCCESS']} 账号信息已保存到 {account_file}")
        return True

    except Exception as e:
        logger.error(f"{EMOJI['ERROR']} 保存账号信息失败: {str(e)}")
        return False

def refresh_token(token, use_proxy=True):
    """刷新token使用中国服务器API
    
    Args:
        token (str): WorkosCursorSessionToken cookie值
        use_proxy (bool): 是否使用代理
        
    Returns:
        str: 刷新后的access token，如果刷新失败则返回原token
    """
    try:
        # 获取代理
        proxy = None
        if use_proxy:
            try:
                # 导入代理管理器
                from api_register.proxy_manager import get_proxy
                proxy = get_proxy()
                if proxy:
                    logger.info(f"{EMOJI['INFO']} 使用代理刷新token: {proxy['http']}")
            except Exception as e:
                logger.warning(f"{EMOJI['WARNING']} 获取代理失败: {str(e)}")
        
        # 刷新服务器URL
        refresh_server = 'https://token.cursorpro.com.cn'
        
        # 确保token格式正确（将::替换为%3A%3A）
        if '%3A%3A' not in token and '::' in token:
            token = token.replace('::', '%3A%3A')
            
        # 请求刷新服务器
        url = f"{refresh_server}/reftoken?token={token}"
        logger.info(f"{EMOJI['INFO']} 正在刷新token...")
        
        import requests
        response = requests.get(url, proxies=proxy, timeout=30)
        
        if response.status_code == 200:
            try:
                import json
                data = response.json()
                
                if data.get('code') == 0 and data.get('msg') == "获取成功":
                    access_token = data.get('data', {}).get('accessToken')
                    days_left = data.get('data', {}).get('days_left', 0)
                    expire_time = data.get('data', {}).get('expire_time', 'Unknown')
                    
                    if access_token:
                        logger.info(f"{EMOJI['SUCCESS']} Token刷新成功! 有效期{days_left}天 (过期时间: {expire_time})")
                        return access_token
                    else:
                        logger.warning(f"{EMOJI['WARNING']} 响应中没有access token")
                else:
                    error_msg = data.get('msg', 'Unknown error')
                    logger.error(f"{EMOJI['ERROR']} Token刷新失败: {error_msg}")
            except json.JSONDecodeError:
                logger.error(f"{EMOJI['ERROR']} 刷新服务器返回了无效的JSON响应")
        else:
            logger.error(f"{EMOJI['ERROR']} 刷新服务器错误: HTTP {response.status_code}")
    
    except requests.exceptions.Timeout:
        logger.error(f"{EMOJI['ERROR']} 刷新服务器请求超时")
    except requests.exceptions.ConnectionError:
        logger.error(f"{EMOJI['ERROR']} 连接刷新服务器失败")
    except Exception as e:
        logger.error(f"{EMOJI['ERROR']} 刷新token时发生错误: {str(e)}")
    
    # 刷新失败时返回原token处理后的部分
    return token.split('%3A%3A')[-1] if '%3A%3A' in token else token.split('::')[-1] if '::' in token else token

def process_token(token, use_proxy=True):
    """处理和刷新token
    
    Args:
        token (str): 原始token或cookie
        use_proxy (bool): 是否使用代理
        
    Returns:
        str: 处理后的token
    """
    try:
        # 尝试刷新token
        refreshed_token = refresh_token(token, use_proxy)
        
        # 如果刷新成功且返回的token不同，使用新token
        if refreshed_token and refreshed_token != token:
            return refreshed_token
        
        # 如果刷新失败，使用传统提取方法
        if '%3A%3A' in token:
            return token.split('%3A%3A')[-1]
        elif '::' in token:
            return token.split('::')[-1]
        else:
            return token
    except Exception as e:
        logger.error(f"{EMOJI['ERROR']} 处理token时发生错误: {str(e)}")
        # 出错时回退到基本提取
        if '%3A%3A' in token:
            return token.split('%3A%3A')[-1]
        elif '::' in token:
            return token.split('::')[-1]
        else:
            return token