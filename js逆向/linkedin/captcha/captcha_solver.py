import json
import os
import time
import requests
from bs4 import BeautifulSoup
import threading
from utils.logger_config import get_logger
from captcha.captcha_async_helper import solve_captcha_async

ASYNC_AVAILABLE = True

# 获取模块日志器
logger = get_logger(__name__)


class CaptchaSolver:
    """
    验证码解决类，用于处理 LinkedIn 的验证码挑战
    """

    def __init__(self, session=None, proxy=None):
        """
        初始化验证码解决器
        
        Args:
            session: 请求会话对象
        """
        # 代理
        self.proxy = proxy
        self.session = session or requests.Session()
        self.api_key = "cf823a34eaea4cd8bb67584c8dd7aeb2764679"
        self.api_url = "http://47.115.166.118:15000/createTask"
        self.result_url = "http://47.115.166.118:15000/getTaskResult"
        self.max_wait_time = 60  # 最大等待时间增加到60秒
        self.check_interval = 3   # 检查间隔
        self.lock = threading.Lock()  # 添加线程锁
        self.log_interval = 15    # 每15秒输出一次详细日志
        self.use_async = True     # 是否使用异步方式处理验证码
        self.concurrent_tasks = 2 # 并发任务数量
        self.max_retries = 3      # 最大重试次数
        self.connection_timeout = 10  # 连接超时时间

        # 从配置文件加载API信息
        self.load_api_config()

    def load_api_config(self):
        """从配置文件加载API配置信息"""
        config_file = 'conf/config.json'
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # 更新API密钥
                if 'api_key' in config and config['api_key']:
                    self.api_key = config['api_key']
                    logger.info("已加载API密钥")

                # 更新API URL（如果在配置中存在）
                if 'api_url' in config and config['api_url']:
                    self.api_url = config['api_url']
                    logger.info(f"已加载API URL: {self.api_url}")

                # 更新结果URL（如果在配置中存在）
                if 'result_url' in config and config['result_url']:
                    self.result_url = config['result_url']
                    logger.info(f"已加载结果URL: {self.result_url}")

                # 更新service URL（如果在配置中存在）
                if 'surl' in config and config['surl']:
                    self.surl = config['surl']
                    logger.info(f"已加载Service URL: {self.surl}")
                
                # 更新超时设置（如果在配置中存在）
                if 'captcha_max_wait_time' in config:
                    self.max_wait_time = config['captcha_max_wait_time']
                    logger.info(f"验证码最大等待时间设置为 {self.max_wait_time} 秒")
                    
                if 'captcha_check_interval' in config:
                    self.check_interval = config['captcha_check_interval']
                    logger.info(f"验证码检查间隔设置为 {self.check_interval} 秒")
                    
                if 'captcha_log_interval' in config:
                    self.log_interval = config['captcha_log_interval']
                    logger.info(f"验证码日志间隔设置为 {self.log_interval} 秒")
                    
                # 加载异步处理配置
                if 'use_async_captcha' in config:
                    self.use_async = config['use_async_captcha']
                    logger.info(f"异步验证码处理: {'启用' if self.use_async else '禁用'}")
                    
                if 'captcha_concurrent_tasks' in config:
                    self.concurrent_tasks = config['captcha_concurrent_tasks']
                    logger.info(f"验证码并发任务数量: {self.concurrent_tasks}")
                    
                if 'captcha_max_retries' in config:
                    self.max_retries = config['captcha_max_retries']
                    logger.info(f"验证码最大重试次数: {self.max_retries}")
                    
                if 'captcha_connection_timeout' in config:
                    self.connection_timeout = config['captcha_connection_timeout']
                    logger.info(f"验证码连接超时: {self.connection_timeout} 秒")
            else:
                logger.warning(f"配置文件 {config_file} 不存在，将使用默认API设置")

        except json.JSONDecodeError:
            logger.error(f"配置文件 {config_file} JSON格式错误")
        except Exception as e:
            logger.error(f"加载API配置时出错: {str(e)}")

    def create_task(self):
        """创建验证任务"""
        with self.lock:  # 使用线程锁保护API调用
            try:
                payload = {
                    "clientKey": self.api_key,
                    "task": {
                        "websiteURL": 'https://www.linkedin.com/checkpoint/challenge/verify',
                        "websiteKey": "6Lc7CQMTAAAAAIL84V_tPRYEWZtljsJQJZ5jSijw",
                        "type": "ReCaptchaV2TaskProxyless",
                    }
                }

                logger.info(f"创建验证任务: {payload}")
                response = requests.post(self.api_url, json=payload, timeout=self.connection_timeout)
                
                if response.status_code != 200:
                    logger.error(f"API请求失败: 状态码 {response.status_code}")
                    return None
                    
                result = response.json()
                logger.info(f"API响应: {result}")

                if result.get("errorId", 1) == 0:
                    task_id = result.get("taskId")
                    logger.info(f"任务ID: {task_id}")
                    return task_id
                else:
                    logger.error(f"API错误: {result.get('errorDescription', '未知错误')}")
                    return None
            except requests.exceptions.Timeout:
                logger.error("创建验证任务超时")
                return None
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {str(e)}")
                return None
            except Exception as e:
                logger.error(f"创建任务出错: {str(e)}")
                return None

    def get_task_result(self, task_id, timeout=None):
        """
        获取验证任务结果
        
        Args:
            task_id: 任务ID
            timeout: 超时时间（秒）
            
        Returns:
            str: 验证码token，如果失败则返回None
        """
        if timeout is None:
            timeout = self.max_wait_time
            
        result_payload = {
            "clientKey": self.api_key,
            "taskId": task_id
        }

        start_time = time.time()
        last_log_time = start_time
        logger.info(f"开始获取验证码结果，等待时间上限：{timeout}秒")
        
        # 使用event避免使用sleep阻塞线程
        stop_event = threading.Event()
        
        check_count = 0
        while not stop_event.is_set() and time.time() - start_time < timeout:
            check_count += 1
            try:
                with self.lock:  # 使用线程锁保护API调用
                    response = requests.post(self.result_url, json=result_payload, timeout=self.connection_timeout)
                    
                    if response.status_code != 200:
                        logger.error(f"获取结果API请求失败: 状态码 {response.status_code}")
                        # 使用Event等待而不是sleep
                        stop_event.wait(self.check_interval)
                        continue
                        
                    result = response.json()
                
                if result.get("errorId", 1) == 0:
                    if result.get("status") == "ready":
                        token = result.get("solution", {}).get("gRecaptchaResponse")
                        if token:
                            logger.info(f"验证码解决成功，token长度: {len(token)}，检查次数: {check_count}")
                            return token
                        else:
                            logger.error("API返回了结果但缺少token")
                            break
                    elif result.get("status") == "processing":
                        current_time = time.time()
                        elapsed = current_time - start_time
                        progress = (elapsed / timeout) * 100
                        
                        # 只在间隔时间后输出日志，减少过多的日志输出
                        if current_time - last_log_time >= self.log_interval:
                            logger.info(f"验证码仍在处理中... 已等待{elapsed:.1f}秒 ({progress:.1f}%)，检查次数：{check_count}")
                            last_log_time = current_time
                            
                        # 使用Event等待而不是sleep
                        remaining = timeout - (current_time - start_time)
                        wait_time = min(self.check_interval, max(0.1, remaining))
                        stop_event.wait(wait_time)
                    else:
                        logger.warning(f"未知状态: {result.get('status')}")
                        stop_event.wait(self.check_interval)
                else:
                    error_desc = result.get('errorDescription', '未知错误')
                    error_id = result.get('errorId')
                    logger.error(f"获取任务结果错误: {error_desc} (错误ID: {error_id})")
                    
                    # 如果是因为任务不存在或已过期，可能需要重新创建任务
                    if "NOT_FOUND" in error_desc or error_id == 16:
                        logger.warning("任务不存在或已过期")
                    
                    break
            except requests.exceptions.Timeout:
                logger.warning(f"获取结果请求超时 (检查#{check_count})，重试...")
                stop_event.wait(1)  # 短暂等待后重试
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {str(e)}")
                stop_event.wait(2)  # 发生异常时等待时间稍长
            except Exception as e:
                logger.error(f"获取结果时出错: {str(e)}")
                stop_event.wait(2)
        
        elapsed = time.time() - start_time
        logger.error(f"验证码解决超时，已等待 {elapsed:.1f} 秒，共检查 {check_count} 次")
        return None

    def create_and_solve_async(self):
        """
        使用异步方式创建并解决验证码任务
        
        Returns:
            str: 验证码token，如果失败则返回None
        """
        if not ASYNC_AVAILABLE:
            logger.warning("异步验证码处理模块不可用，将使用同步方式")
            return None
            
        try:
            # 准备配置字典传递给异步助手
            config = {
                "captcha_max_wait_time": self.max_wait_time,
                "captcha_check_interval": self.check_interval,
                "captcha_concurrent_tasks": self.concurrent_tasks,
                "captcha_max_retries": self.max_retries,
                "captcha_connection_timeout": self.connection_timeout
            }
            
            logger.info(f"使用异步方式处理验证码，并发数量: {self.concurrent_tasks}")
            
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # 在线程中运行异步函数，避免阻塞主线程
                future = executor.submit(
                    solve_captcha_async,
                    self.api_key, 
                    self.api_url, 
                    self.result_url, 
                    timeout=None,  # 使用配置中的值
                    concurrent_tasks=None,  # 使用配置中的值
                    config=config
                )
                
                # 设置超时时间比验证码处理的超时时间略长一点
                result_timeout = self.max_wait_time + 5
                token = future.result(timeout=result_timeout)
            
            if token:
                logger.info("异步验证码处理成功")
                return token
            else:
                logger.warning("异步验证码处理失败，将尝试同步方式")
                return None
        except concurrent.futures.TimeoutError:
            logger.error("异步验证码处理超时")
            return None
        except Exception as e:
            logger.error(f"异步验证码处理出错: {str(e)}")
            return None

    def solve(self, challenge_url):
        """
        解决验证码挑战并完成登录
        
        Args:
            challenge_url: 验证挑战URL
            
        Returns:
            登录成功后的响应
        """
        logger.info(f"开始解决验证挑战: {challenge_url}")

        # 创建重试机制
        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            try:
                # 获取验证页面
                logger.info(f"获取验证页面 (尝试 {attempt}/{max_attempts})...")
                response = self.session.get(challenge_url, allow_redirects=True, timeout=30)
                html_content = response.text
                logger.info(f"验证页面响应状态: {response.status_code}, 最终URL: {response.url}")

                soup = BeautifulSoup(html_content, 'html.parser')

                # 检查是否有错误消息
                error_div = soup.find('div', {'id': 'error-for-password'}) or soup.find('div', {'role': 'alert'})
                if error_div:
                    error_text = error_div.get_text(strip=True)
                    logger.warning(f"发现错误信息: {error_text}")
                    return {"type": "error", "message": error_text}

                # 提取所有隐藏的输入字段
                form_params = {}
                for input_tag in soup.find_all('input', {'type': 'hidden'}):
                    name = input_tag.get('name')
                    value = input_tag.get('value', '')
                    if name:
                        form_params[name] = value
                logger.debug(f"发现 {len(form_params)} 个表单参数")
                logger.info("检测到验证码挑战，开始处理...")
                
                # 尝试使用异步方式获取验证码token
                token = None
                if self.use_async and ASYNC_AVAILABLE:
                    token = self.create_and_solve_async()
                
                # 如果异步方式失败，则使用传统方式
                if not token:
                    # 创建验证任务
                    task_id = self.create_task()
                    if not task_id:
                        logger.error("创建验证任务失败")
                        if attempt < max_attempts:
                            # 使用Event等待而不是sleep
                            retry_wait = threading.Event()
                            logger.info(f"将在5秒后重试... ({attempt}/{max_attempts})")
                            retry_wait.wait(5)
                            continue
                        return None

                    # 获取验证结果
                    token = self.get_task_result(task_id)
                    if not token:
                        logger.error("获取验证结果失败")
                        if attempt < max_attempts:
                            # 使用Event等待而不是sleep
                            retry_wait = threading.Event()
                            logger.info(f"将在5秒后重试... ({attempt}/{max_attempts})")
                            retry_wait.wait(5)
                            continue
                        return None

                logger.info(f"成功获取验证码令牌，准备提交验证结果")

                # 准备完整的提交数据
                submit_data = {
                    'csrfToken': form_params.get('csrfToken', ''),
                    'captchaSiteKey': form_params.get('captchaSiteKey', '6Lc7CQMTAAAAAIL84V_tPRYEWZtljsJQJZ5jSijw'),
                    'challengeId': form_params.get('challengeId', ''),
                    'language': form_params.get('language', 'zh-CN'),
                    'displayTime': form_params.get('displayTime', ''),
                    'challengeType': form_params.get('challengeType', ''),
                    'challengeSource': form_params.get('challengeSource', ''),
                    'requestSubmissionId': form_params.get('requestSubmissionId', ''),
                    'captchaUserResponseToken': token,
                    'challengeData': form_params.get('challengeData', ''),
                    'pageInstance': form_params.get('pageInstance', ''),
                    'challengeDetails': form_params.get('challengeDetails', ''),
                    'failureRedirectUri': form_params.get('failureRedirectUri', ''),
                    'flowTreeId': form_params.get('flowTreeId', ''),
                    'signInLink': form_params.get('signInLink', '/checkpoint/lg/login?trk=hb_signin'),
                    'joinNowLink': form_params.get('joinNowLink', '/signup/cold-join'),
                    '_s': form_params.get('_s', 'CONSUMER_LOGIN'),
                }

                logger.info("准备提交验证数据")

                # 提交验证结果
                verify_response = self.session.post(
                    'https://www.linkedin.com/checkpoint/challenge/verify',
                    data=submit_data,
                    allow_redirects=True,
                    proxies=self.proxy,
                    timeout=30  # 添加超时
                )

                logger.info(f"验证提交响应状态: {verify_response.status_code}, URL: {verify_response.url}")
                
                # 检查响应中是否包含成功标识
                if 'feed' in verify_response.url or 'mynetwork' in verify_response.url:
                    logger.info("验证成功，已进入LinkedIn主页")
                else:
                    logger.info(f"验证已提交，最终URL: {verify_response.url}")

                return verify_response
                
            except requests.exceptions.Timeout:
                logger.error("验证码解决过程超时")
                if attempt < max_attempts:
                    # 使用Event等待而不是sleep
                    retry_wait = threading.Event()
                    logger.info(f"将在5秒后重试... ({attempt}/{max_attempts})")
                    retry_wait.wait(5)
                else:
                    return {"type": "error", "message": "验证码解决超时"}
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {str(e)}")
                if attempt < max_attempts:
                    # 使用Event等待而不是sleep
                    retry_wait = threading.Event()
                    logger.info(f"将在5秒后重试... ({attempt}/{max_attempts})")
                    retry_wait.wait(5)
                else:
                    return {"type": "error", "message": f"请求异常: {str(e)}"}
            except Exception as e:
                logger.error(f"验证码解决出错: {str(e)}")
                if attempt < max_attempts:
                    # 使用Event等待而不是sleep
                    retry_wait = threading.Event()
                    logger.info(f"将在5秒后重试... ({attempt}/{max_attempts})")
                    retry_wait.wait(5)
                else:
                    return {"type": "error", "message": f"验证码解决出错: {str(e)}"}
                    
        return {"type": "error", "message": "验证码解决失败，已达到最大重试次数"}
