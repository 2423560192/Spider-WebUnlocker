import asyncio
import aiohttp
import json
import time
import threading
import random
from utils.logger_config import get_logger

# 获取模块日志器
logger = get_logger(__name__)

class AsyncCaptchaHelper:
    """
    异步验证码处理助手，使用协程优化验证码请求处理
    """
    def __init__(self, api_key, api_url, result_url):
        """
        初始化异步验证码助手
        
        Args:
            api_key: API密钥
            api_url: 创建任务的API URL
            result_url: 获取结果的API URL
        """
        self.api_key = api_key
        self.api_url = api_url
        self.result_url = result_url
        self.lock = threading.Lock()
        self.max_concurrent_tasks = 3  # 最大并发任务数
        self.timeout = 60  # 默认超时时间（秒）
        self.check_interval = 3  # 检查结果间隔（秒）
        self.max_retries = 3     # 最大重试次数
        self.connection_timeout = 10  # 连接超时时间（秒）
        self.performance_logs = {}  # 存储性能数据的字典
        
    def set_params_from_config(self, config):
        """
        从配置文件设置参数
        
        Args:
            config: 配置字典
        """
        if config:
            self.timeout = config.get("captcha_max_wait_time", self.timeout)
            self.check_interval = config.get("captcha_check_interval", self.check_interval)
            self.max_retries = config.get("captcha_max_retries", self.max_retries)
            self.max_concurrent_tasks = config.get("captcha_concurrent_tasks", self.max_concurrent_tasks)
            self.connection_timeout = config.get("captcha_connection_timeout", self.connection_timeout)
            logger.info(f"从配置加载验证码参数: 超时={self.timeout}秒, 重试={self.max_retries}次, 并发={self.max_concurrent_tasks}个")
        
    async def async_create_task(self, session, website_url="https://www.linkedin.com/checkpoint/challenge/verify", 
                              website_key="6Lc7CQMTAAAAAIL84V_tPRYEWZtljsJQJZ5jSijw", retry_count=2):
        """
        异步创建验证码任务，带有智能重试
        
        Args:
            session: aiohttp.ClientSession对象
            website_url: 验证码所在网页URL
            website_key: 验证码站点密钥
            retry_count: 最大重试次数
            
        Returns:
            str: 任务ID，如果失败则返回None
        """
        start_time = time.time()
        self.performance_logs["create_task_start"] = start_time
        
        for attempt in range(1, retry_count + 1):
            try:
                payload = {
                    "clientKey": self.api_key,
                    "task": {
                        "websiteURL": website_url,
                        "websiteKey": website_key,
                        "type": "ReCaptchaV2TaskProxyless",
                    }
                }
                
                logger.info(f"异步创建验证任务 (尝试 {attempt}/{retry_count})...")
                api_call_start = time.time()
                
                # 使用超时参数
                async with session.post(self.api_url, json=payload, timeout=self.connection_timeout) as response:
                    api_response_time = time.time() - api_call_start
                    logger.info(f"API响应时间: {api_response_time:.2f}秒")
                    
                    if response.status != 200:
                        logger.error(f"API请求失败: 状态码 {response.status}")
                        if attempt < retry_count:
                            # 使用指数退避算法
                            backoff_time = (2 ** (attempt - 1)) * 1.5 + random.uniform(0, 0.5)
                            logger.info(f"将在 {backoff_time:.2f} 秒后重试...")
                            await asyncio.sleep(backoff_time)
                            continue
                        return None
                        
                    result = await response.json()
                    
                    if result.get("errorId", 1) == 0:
                        task_id = result.get("taskId")
                        total_time = time.time() - start_time
                        logger.info(f"异步创建任务成功，ID: {task_id}，耗时: {total_time:.2f}秒")
                        self.performance_logs["create_task_end"] = time.time()
                        self.performance_logs["create_task_duration"] = total_time
                        return task_id
                    else:
                        error_msg = result.get('errorDescription', '未知错误')
                        error_id = result.get('errorId')
                        logger.error(f"API错误: {error_msg} (错误ID: {error_id})")
                        
                        if error_id == 2: # 通常表示验证失败
                            logger.error("API密钥验证失败，请检查密钥是否正确")
                            return None  # 直接退出，不再重试
                        
                        if error_id == 10: # 通常表示余额不足
                            logger.error("API账户余额不足")
                            return None  # 直接退出，不再重试
                        
                        if attempt < retry_count:
                            # 使用指数退避算法
                            backoff_time = (2 ** (attempt - 1)) * 1.5 + random.uniform(0, 0.5)
                            logger.info(f"将在 {backoff_time:.2f} 秒后重试...")
                            await asyncio.sleep(backoff_time)
                        else:
                            return None
                        
            except asyncio.TimeoutError:
                logger.error(f"创建验证任务请求超时 (尝试 {attempt}/{retry_count})")
                if attempt < retry_count:
                    # 使用指数退避算法
                    backoff_time = (2 ** (attempt - 1)) * 1.5 + random.uniform(0, 0.5)
                    logger.info(f"将在 {backoff_time:.2f} 秒后重试...")
                    await asyncio.sleep(backoff_time)
                else:
                    return None
            except Exception as e:
                logger.error(f"创建任务出错: {str(e)} (尝试 {attempt}/{retry_count})")
                if attempt < retry_count:
                    # 使用指数退避算法
                    backoff_time = (2 ** (attempt - 1)) * 1.5 + random.uniform(0, 0.5)
                    logger.info(f"将在 {backoff_time:.2f} 秒后重试...")
                    await asyncio.sleep(backoff_time)
                else:
                    return None
                    
        return None
    
    async def async_get_task_result(self, session, task_id, timeout=None):
        """
        异步获取验证码任务结果
        
        Args:
            session: aiohttp.ClientSession对象
            task_id: 任务ID
            timeout: 超时时间（秒）
            
        Returns:
            str: 验证码token，如果失败则返回None
        """
        if timeout is None:
            timeout = self.timeout
        
        result_payload = {
            "clientKey": self.api_key,
            "taskId": task_id
        }
        
        start_time = time.time()
        self.performance_logs["get_result_start"] = start_time
        logger.info(f"开始异步获取验证码结果，最长等待{timeout}秒")
        
        check_count = 0
        last_status_time = start_time
        
        while time.time() - start_time < timeout:
            check_count += 1
            check_start_time = time.time()
            
            try:
                async with session.post(self.result_url, json=result_payload, timeout=self.connection_timeout) as response:
                    check_response_time = time.time() - check_start_time
                    
                    # 每10次检查记录一次响应时间
                    if check_count % 10 == 1:
                        logger.info(f"检查#{check_count} - API响应时间: {check_response_time:.2f}秒")
                    
                    if response.status != 200:
                        logger.error(f"获取结果API请求失败: 状态码 {response.status}")
                        await asyncio.sleep(self.check_interval)
                        continue
                        
                    result = await response.json()
                    
                    if result.get("errorId", 1) == 0:
                        if result.get("status") == "ready":
                            token = result.get("solution", {}).get("gRecaptchaResponse")
                            if token:
                                elapsed = time.time() - start_time
                                logger.info(f"验证码解决成功，总用时{elapsed:.1f}秒，共检查{check_count}次")
                                self.performance_logs["get_result_end"] = time.time()
                                self.performance_logs["get_result_duration"] = elapsed
                                self.performance_logs["result_check_count"] = check_count
                                return token
                            else:
                                logger.error("API返回了结果但缺少token")
                                break
                        elif result.get("status") == "processing":
                            current_time = time.time()
                            elapsed = current_time - start_time
                            progress = (elapsed / timeout) * 100
                            
                            # 每15秒输出一次详细日志
                            if current_time - last_status_time >= 15:
                                logger.info(f"验证码仍在处理中... 已等待{elapsed:.1f}秒 ({progress:.1f}%)，检查次数：{check_count}")
                                last_status_time = current_time
                            else:
                                logger.debug(f"验证码处理中 - {elapsed:.1f}秒/{timeout}秒")
                                
                            await asyncio.sleep(self.check_interval)
                        else:
                            logger.warning(f"未知状态: {result.get('status')}")
                            await asyncio.sleep(self.check_interval)
                    else:
                        error_desc = result.get('errorDescription', '未知错误')
                        error_id = result.get('errorId')
                        logger.error(f"获取任务结果错误: {error_desc} (错误ID: {error_id})")
                        
                        # 如果任务不存在，直接退出
                        if "NOT_FOUND" in error_desc or error_id == 16:
                            logger.error("任务不存在或已过期")
                            break
                        
                        await asyncio.sleep(self.check_interval)
                        
            except asyncio.TimeoutError:
                logger.warning(f"获取结果请求超时 (检查#{check_count})，重试...")
                await asyncio.sleep(min(2, self.check_interval))
            except Exception as e:
                logger.error(f"获取结果时出错: {str(e)}")
                await asyncio.sleep(min(2, self.check_interval))
                
        final_elapsed = time.time() - start_time
        logger.error(f"验证码解决超时，已等待{final_elapsed:.1f}秒，共尝试检查{check_count}次")
        self.performance_logs["result_timeout"] = True
        self.performance_logs["result_check_count"] = check_count
        return None
    
    async def _process_single_captcha(self, website_url, website_key):
        """
        处理单个验证码任务
        
        Args:
            website_url: 验证码所在网页URL
            website_key: 验证码站点密钥
            
        Returns:
            str: 验证码token，如果失败则返回None
        """
        # 使用超时设置创建ClientSession
        timeout = aiohttp.ClientTimeout(total=self.timeout+15, connect=self.connection_timeout, 
                                       sock_connect=self.connection_timeout, sock_read=self.connection_timeout)
        conn = aiohttp.TCPConnector(limit=5, ssl=False)
        
        try:
            task_start_time = time.time()
            
            # 使用配置好的会话
            async with aiohttp.ClientSession(timeout=timeout, connector=conn) as session:
                # 创建任务
                task_id = await self.async_create_task(session, website_url, website_key, retry_count=self.max_retries)
                if not task_id:
                    logger.error("创建验证码任务失败")
                    return None
                    
                # 获取结果
                token = await self.async_get_task_result(session, task_id)
                if token:
                    total_time = time.time() - task_start_time
                    logger.info(f"验证码任务完成，总耗时: {total_time:.2f}秒")
                    self.performance_logs["total_duration"] = total_time
                    return token
                    
                logger.error("获取验证码结果失败")
                return None
        except Exception as e:
            logger.error(f"处理验证码任务时发生错误: {str(e)}")
            return None
    
    async def solve_multiple_parallel(self, count=3):
        """
        并行处理多个验证码任务，返回第一个成功的结果
        
        Args:
            count: 并行处理的任务数量
            
        Returns:
            str: 第一个成功的验证码token，全部失败则返回None
        """
        website_url = "https://www.linkedin.com/checkpoint/challenge/verify"
        website_key = "6Lc7CQMTAAAAAIL84V_tPRYEWZtljsJQJZ5jSijw"
        
        parallel_start = time.time()
        logger.info(f"并行处理{count}个验证码任务...")
        tasks = [self._process_single_captcha(website_url, website_key) for _ in range(count)]
        
        # 等待第一个完成的任务
        try:
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            
            # 取消其他任务
            for task in pending:
                task.cancel()
                
            # 处理完成的任务
            for task in done:
                try:
                    result = task.result()
                    if result:
                        parallel_time = time.time() - parallel_start
                        logger.info(f"获取到验证码结果，用时{parallel_time:.2f}秒，取消其他并行任务")
                        self.performance_logs["parallel_duration"] = parallel_time
                        return result
                except Exception as e:
                    logger.error(f"任务执行异常: {str(e)}")
                    
            logger.error("所有并行任务均失败")
            return None
        except Exception as e:
            logger.error(f"并行处理验证码任务时出错: {str(e)}")
            return None

    def get_captcha_token(self, concurrent_tasks=None, timeout=None, config=None):
        """
        获取验证码token的主入口方法
        
        Args:
            concurrent_tasks: 并行任务数量
            timeout: 超时时间（秒）
            config: 配置字典
            
        Returns:
            str: 验证码token，如果失败则返回None
        """
        # 保存原始设置
        original_timeout = self.timeout
        original_concurrent = self.max_concurrent_tasks
        
        # 如果有配置字典，应用配置
        if config:
            self.set_params_from_config(config)
            
        # 参数优先级: 函数参数 > 配置文件 > 默认值
        if concurrent_tasks is None:
            concurrent_tasks = self.max_concurrent_tasks
        if timeout is None:
            timeout = self.timeout
            
        self.performance_logs = {}  # 重置性能日志
        
        try:
            # 记录开始时间
            overall_start = time.time()
            self.performance_logs["overall_start"] = overall_start
            
            # 更新超时设置
            self.timeout = timeout
            logger.info(f"开始获取验证码，并发任务数:{concurrent_tasks}，超时:{timeout}秒")
            
            # 运行异步任务
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                token = loop.run_until_complete(self.solve_multiple_parallel(concurrent_tasks))
                if token:
                    overall_time = time.time() - overall_start
                    logger.info(f"验证码获取成功，总耗时: {overall_time:.2f}秒")
                    self.performance_logs["overall_end"] = time.time()
                    self.performance_logs["overall_duration"] = overall_time
                    return token
                else:
                    logger.error("获取验证码失败")
                    return None
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"验证码处理出错: {str(e)}")
            return None
        finally:
            # 还原原始设置
            self.timeout = original_timeout
            self.max_concurrent_tasks = original_concurrent

# 示例用法
def solve_captcha_async(api_key, api_url, result_url, timeout=None, concurrent_tasks=None, config=None):
    """
    使用异步方式解决验证码
    
    Args:
        api_key: API密钥
        api_url: 创建任务的API URL
        result_url: 获取结果的API URL
        timeout: 超时时间（秒）
        concurrent_tasks: 并发任务数
        config: 配置字典
        
    Returns:
        str: 验证码token，如果失败则返回None
    """
    helper = AsyncCaptchaHelper(api_key, api_url, result_url)
    return helper.get_captcha_token(concurrent_tasks, timeout, config) 