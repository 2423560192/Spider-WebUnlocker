import pandas as pd
import random
import uuid
import concurrent.futures
import threading
from core.linkedin_unlocker import LinkedInUnlocker
from bs4 import BeautifulSoup
import requests
from utils.thread_pool import ThreadPoolManager
from utils.logger_config import get_logger

# 获取模块日志器
logger = get_logger(__name__)

# 创建全局线程锁，用于同步Excel文件写入
excel_lock = threading.Lock()

# 常用浏览器的User-Agent列表
USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:118.0) Gecko/20100101 Firefox/118.0",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]


def get_random_user_agent():
    """获取随机User-Agent"""
    return random.choice(USER_AGENTS)


def judge_login_response(response):
    """
    判断LinkedIn登录响应的状态

    Args:
        response: requests.Response对象

    Returns:
        str: 登录结果描述
    """
    if not isinstance(response, requests.Response):
        return "无效响应"

    # 解析响应内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. 根据URL判断登录状态
    if 'feed' in response.url or 'mynetwork' in response.url or '/home' in response.url:
        return "登录成功"

    # 2. 检查关键cookie - LinkedIn成功登录后会设置li_at cookie
    if response.cookies.get("li_at", ""):
        return "登录成功"

    # 3. 检查是否是标准登录页面
    login_form = soup.find('form', {'class': 'login__form'})
    if login_form and 'login' in response.url:
        # 检查密码错误
        password_error = soup.find('div', {'id': 'error-for-password'})
        if password_error and 'hidden__imp' not in password_error.get('class', []):
            error_msg = password_error.get_text(strip=True)
            return "用户名或密码错误"

        # 检查用户名错误
        username_error = soup.find('div', {'id': 'error-for-username'})
        if username_error and 'hidden__imp' not in username_error.get('class', []):
            error_msg = username_error.get_text(strip=True)
            return "用户名或密码错误"

        # 如果没有错误信息，则为标准登录页面
        return "异常"

    # 4. 检查错误提示"出现问题，请重试"（服务器错误）
    page_text = soup.get_text(strip=True)
    if "出现问题，请重试" in page_text:
        return "登录异常"

    # 5. 检查是否在验证页面
    if 'checkpoint' in response.url:
        # 检查验证码挑战
        if soup.find('form', {'id': 'captcha-challenge'}) or "captcha" in response.url.lower():
            return "继续验证"

        # 寻找标题元素，但排除普通登录页面
        title_elem = soup.find('h1') or soup.find('h2')
        if title_elem:
            title_text = title_elem.get_text(strip=True)
            # 确保不是普通登录页面的"登录"标题
            if title_text != "登录" or "验证" in page_text:
                return f"继续验证"

    if "帐号已被暂时锁定" in response.text:
        return '继续验证'

    # 7. 检查红色错误提示框
    error_banner = soup.find('div', {'class': 'body__banner--error'})
    if error_banner and 'hidden__imp' not in error_banner.get('class', []):
        error_msg = error_banner.get_text(strip=True)
        return f"登录异常"

    # 8. 检查是否有表单问题
    if 'form__input--error' in response.text:
        return "用户名或密码错误"

    # 9. 默认情况
    return "异常"


def login_account_async(task_info):
    """
    异步登录单个LinkedIn账号并保存结果
    
    Args:
        task_info: 包含任务信息的字典，包括username, password, output_dir
        
    Returns:
        tuple: (响应内容, 登录状态描述, 验证方式)
    """
    username = task_info['username']
    password = task_info['password']
    output_dir = task_info['output_dir']

    logger.info(f"开始登录账号: {username}")

    # 确保账号输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 重试机制相关参数
    max_retry_count = 1  # 最大重试次数
    current_retry = 0
    retry_delay = 5  # 初始重试延迟(秒)

    while current_retry <= max_retry_count:
        try:
            # 获取随机UA
            random_ua = get_random_user_agent()
            logger.debug(f"使用随机UA: {random_ua}")

            # 创建LinkedIn解锁器实例
            unlocker = LinkedInUnlocker(random_ua, username, password)

            # 执行登录
            login_response = unlocker.login()

            # 保存登录HTML结果
            final_html_path = os.path.join(output_dir, 'final_login.html')

            # 保存最终登录响应
            if hasattr(login_response, 'text'):
                with open(final_html_path, 'w', encoding='utf-8') as f:
                    f.write(login_response.text)
                logger.debug(f"已保存最终登录HTML到: {final_html_path}")

            # 判断登录状态
            login_status = judge_login_response(login_response)

            # 检查验证方式
            verification_method = '无'
            if login_status == '继续验证' and hasattr(login_response, 'text'):
                if '帐号受限' in login_response.text:
                    verification_method = '帐号受限'
                elif '查看您的领英' in login_response.text:
                    verification_method = 'Linkedin-app验证'
                elif '邮箱' in login_response.text:
                    verification_method = '邮箱验证'
                elif '验证器' in login_response.text:
                    verification_method = '验证器APP验证'
                elif '手机' in login_response.text:
                    verification_method = '手机验证'

            # 更新的结果检查逻辑 - 只有在特定状态下才进行重试
            if "登录成功" in login_status:
                logger.info(f"账号 {username} 登录成功")
                # 立即保存登录成功的账号到Excel
                save_account_to_txt(username, password, login_status, verification_method)
                return login_response.text, login_status, verification_method
            elif "继续验证" in login_status:
                logger.info(f"账号 {username} 需要继续验证: {login_status}, 验证方式: {verification_method}")
                # 立即保存需要验证的账号到Excel
                save_account_to_txt(username, password, login_status, verification_method)
                return login_response.text, login_status, verification_method
            elif "用户名或密码错误" in login_status:
                logger.warning(f"账号 {username} 用户名或密码错误")
                # 立即保存密码错误的账号到Excel
                save_account_to_txt(username, password, login_status, verification_method)
                return login_response.text, login_status, verification_method
            else:
                # 只有在特定错误状态下才尝试重试
                current_retry += 1
                if current_retry <= max_retry_count:
                    # 使用Event等待替代time.sleep，避免阻塞线程
                    wait_event = threading.Event()
                    # 指数退避重试
                    wait_time = retry_delay * (2 ** (current_retry - 1))
                    logger.warning(
                        f"账号 {username} 登录状态异常({login_status})，将在 {wait_time} 秒后重试 ({current_retry}/{max_retry_count})")
                    wait_event.wait(wait_time)
                else:
                    logger.error(f"账号 {username} 在 {max_retry_count} 次尝试后仍然登录状态异常: {login_status}")
                    # 保存登录异常的账号到Excel
                    save_account_to_txt(username, password, login_status, verification_method)
                    return login_response.text, login_status, verification_method

        except Exception as e:
            current_retry += 1
            if current_retry <= max_retry_count:
                # 使用Event等待替代time.sleep，避免阻塞线程
                wait_event = threading.Event()
                # 指数退避重试
                wait_time = retry_delay * (2 ** (current_retry - 1))
                logger.warning(
                    f"账号 {username} 登录出错，将在 {wait_time} 秒后重试 ({current_retry}/{max_retry_count}): {str(e)}")
                wait_event.wait(wait_time)
            else:
                logger.error(f"账号 {username} 在 {max_retry_count} 次尝试后仍然出错: {str(e)}")
                import traceback
                traceback.print_exc()
                error_status = f"程序错误: {str(e)}"
                # 保存出错的账号到Excel
                save_account_to_txt(username, password, error_status, '无')
                return False, error_status, '无'

    failure_status = "达到最大重试次数"
    # 保存重试失败的账号到Excel
    save_account_to_txt(username, password, failure_status, '无')
    return False, failure_status, '无'


def batch_login(accounts_file, output_root, delay=30, max_concurrent=5):
    """
    批量登录LinkedIn账号，使用线程池异步处理
    
    Args:
        accounts_file: 包含账号信息的文件路径
        output_root: 输出根目录
        delay: 提交任务之间的延迟(秒)
        max_concurrent: 最大并发任务数
        
    Returns:
        dict: 登录结果统计和Excel数据
    """
    # 确保输出根目录存在
    os.makedirs(output_root, exist_ok=True)

    # 初始化线程池
    thread_pool_manager = ThreadPoolManager(max_workers=max_concurrent)
    thread_pool_manager.start()

    # 添加处理过的账号跟踪字典
    processed_accounts = {}
    
    # 先从已保存的txt文件中读取已处理过的账号信息
    txt_path = '登录结果报告.txt'
    if os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # 跳过标题行
                if len(lines) > 0:
                    for i, line in enumerate(lines):
                        if i == 0:  # 跳过标题行
                            continue
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split('----')
                        if len(parts) >= 4:
                            username = parts[0].strip()
                            password = parts[1].strip()
                            status = parts[2].strip()
                            processed_accounts[username] = {
                                'password': password,
                                'status': status
                            }
            logger.info(f"已从文本文件中读取 {len(processed_accounts)} 个账号信息")
        except Exception as e:
            logger.error(f"读取已有文本文件失败: {str(e)}")

    # 读取账号信息
    accounts = []
    try:
        with open(accounts_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 解析账号信息
                if ',' in line:
                    username, password = line.split(',', 1)
                else:
                    parts = line.split()
                    if len(parts) >= 2:
                        username = parts[0].strip()
                        password = parts[1].strip()
                    else:
                        logger.warning(f"忽略格式不正确的行: {line}")
                        continue

                accounts.append((username.strip(), password.strip()))

        logger.info(f"成功加载 {len(accounts)} 个账号")
    except Exception as e:
        logger.error(f"读取账号文件失败: {str(e)}")
        return {"成功": 0, "失败": 0, "总计": 0, "excel_data": None}

    # 准备Excel表格数据
    excel_data = {
        "账号": [],
        "密码": [],
        "登录状态": [],
        "验证方式": [],
    }

    # 统计结果
    results = {"成功": 0, "失败": 0, "总计": len(accounts), "跳过": 0}

    # 任务列表和Future对象字典
    task_futures = {}

    try:
        # 提交所有账号登录任务
        for i, (username, password) in enumerate(accounts):
            # 检查账号是否已经处理过
            if username in processed_accounts:
                # 检查密码是否相同
                if processed_accounts[username]['password'] == password:
                    logger.info(f"账号 {username} 已经处理过且密码相同，跳过该账号")
                    results["跳过"] += 1
                    
                    # 更新统计
                    status = processed_accounts[username]['status']
                    if "登录成功" in status or "继续验证" in status:
                        results["成功"] += 1
                    else:
                        results["失败"] += 1
                    continue
                else:
                    logger.info(f"账号 {username} 已处理过但密码不同，将重新处理")

            # # 账号目录名
            account_dir = os.path.join(output_root, f"{username.replace('@', '_at_')}")

            # 创建任务信息
            task_info = {
                'username': username,
                'password': password,
                'output_dir': account_dir,
                'task_id': str(uuid.uuid4())
            }

            # 提交任务
            future = thread_pool_manager.submit_task(login_account_async, task_info)
            task_futures[username] = future

            logger.info(f"已提交账号 {username} 的登录任务 ({i + 1}/{len(accounts)})")

            # 延迟提交下一个任务，避免过于频繁
            if i < len(accounts) - 1 and delay > 0:
                # 使用Event等待替代time.sleep，避免阻塞线程
                wait_event = threading.Event()
                wait_event.wait(delay)

        # 等待并收集所有任务结果 - 仅收集统计信息，因为保存已在每个任务中完成
        for username, future in task_futures.items():
            try:
                # 等待任务完成，设置超时时间防止无限等待
                result = future.result(timeout=300)  # 5分钟超时

                if result:
                    final_html, status, verification_method = result

                    # 记录账号处理结果，避免重复处理
                    processed_accounts[username] = {
                        'password': next((password for u, password in accounts if u == username), ""),
                        'status': status
                    }

                    # 记录Excel数据 - 只为统计用途，实际已经实时保存
                    excel_data["账号"].append(username)
                    excel_data["密码"].append(next((password for u, password in accounts if u == username), ""))
                    excel_data["登录状态"].append(status)
                    excel_data["验证方式"].append(verification_method)

                    if "登录成功" in status or "继续验证" in status:
                        results["成功"] += 1
                        logger.info(f"账号 {username} 登录成功或需验证: {status}, 验证方式: {verification_method}")
                    else:
                        results["失败"] += 1
                        logger.warning(f"账号 {username} 登录失败: {status}")
                else:
                    # 任务执行失败但没有抛出异常
                    results["失败"] += 1
                    excel_data["账号"].append(username)
                    excel_data["密码"].append(next((password for u, password in accounts if u == username), ""))
                    excel_data["登录状态"].append("未知错误")
                    excel_data["验证方式"].append("无")
                    # 记录账号处理结果
                    processed_accounts[username] = {
                        'password': next((password for u, password in accounts if u == username), ""),
                        'status': "未知错误"
                    }
                    logger.warning(f"账号 {username} 任务执行失败，未返回结果")
            except concurrent.futures.TimeoutError:
                results["失败"] += 1
                excel_data["账号"].append(username)
                excel_data["密码"].append(next((password for u, password in accounts if u == username), ""))
                excel_data["登录状态"].append("任务超时")
                excel_data["验证方式"].append("无")
                # 记录账号处理结果
                processed_accounts[username] = {
                    'password': next((password for u, password in accounts if u == username), ""),
                    'status': "任务超时"
                }
                # 保存超时账号到Excel
                password_str = next((password for u, password in accounts if u == username), "")
                save_account_to_txt(username, password_str, "任务超时", "无")
                logger.error(f"账号 {username} 任务执行超时")
            except Exception as e:
                results["失败"] += 1
                excel_data["账号"].append(username)
                excel_data["密码"].append(next((password for u, password in accounts if u == username), ""))
                excel_data["登录状态"].append(f"程序错误: {str(e)}")
                excel_data["验证方式"].append("无")
                # 记录账号处理结果
                processed_accounts[username] = {
                    'password': next((password for u, password in accounts if u == username), ""),
                    'status': f"程序错误: {str(e)}"
                }
                # 保存出错账号到Excel
                password_str = next((password for u, password in accounts if u == username), "")
                save_account_to_txt(username, password_str, f"程序错误: {str(e)}", "无")
                logger.error(f"账号 {username} 任务执行异常: {str(e)}")

    except KeyboardInterrupt:
        logger.info("接收到中断信号，停止批量登录")

        # 检查是否有已完成的任务结果
        for username, future in task_futures.items():
            if future.done():
                try:
                    result = future.result(timeout=1)  # 快速检查结果
                    if result and username not in excel_data["账号"]:
                        final_html, status, verification_method = result
                        excel_data["账号"].append(username)
                        excel_data["密码"].append(next((password for u, password in accounts if u == username), ""))
                        excel_data["登录状态"].append(status)
                        excel_data["验证方式"].append(verification_method)

                        # 记录账号处理结果
                        processed_accounts[username] = {
                            'password': next((password for u, password in accounts if u == username), ""),
                            'status': status
                        }

                        if "登录成功" in status or "继续验证" in status:
                            results["成功"] += 1
                        else:
                            results["失败"] += 1
                except Exception:
                    # 忽略获取结果时的错误
                    pass
            else:
                # 将未完成的任务标记为"已中断"
                if username not in excel_data["账号"]:
                    excel_data["账号"].append(username)
                    excel_data["密码"].append(next((password for u, password in accounts if u == username), ""))
                    excel_data["登录状态"].append("任务已中断")
                    excel_data["验证方式"].append("无")
                    # 记录账号处理结果
                    processed_accounts[username] = {
                        'password': next((password for u, password in accounts if u == username), ""),
                        'status': "任务已中断"
                    }
                    # 保存中断账号到Excel
                    password_str = next((password for u, password in accounts if u == username), "")
                    save_account_to_txt(username, password_str, "任务已中断", "无")
                    results["失败"] += 1

    finally:
        # 确保至少有一条记录，防止Excel为空
        if not excel_data["账号"]:
            for username, password in accounts:
                if username not in processed_accounts:
                    excel_data["账号"].append(username)
                    excel_data["密码"].append(password)
                    excel_data["登录状态"].append("程序被中断，未执行")
                    excel_data["验证方式"].append("无")
                    # 保存未执行账号到Excel
                    save_account_to_txt(username, password, "程序被中断，未执行", "无")
            results["失败"] = len(accounts) - results["跳过"]

        # 停止线程池
        thread_pool_manager.stop()
        logger.info("=" * 50)
        logger.info("批量登录完成!")

    # 输出统计结果
    logger.info(f"批量登录完成，成功: {results['成功']}/{results['总计']}, 失败: {results['失败']}/{results['总计']}, 跳过: {results['跳过']}/{results['总计']}")

    # 添加Excel数据到结果
    results["excel_data"] = excel_data
    return results


def save_account_to_txt(username, password, status, verification_method):
    """
    将单个账号的登录结果保存到文本文件
    
    Args:
        username: 账号用户名
        password: 账号密码
        status: 登录状态
        verification_method: 验证方式
        
    Returns:
        bool: 保存是否成功
    """
    # 文本文件统一保存在根目录，文件名为'登录结果报告.txt'
    txt_path = '登录结果报告.txt'
    
    # 使用线程锁保护文件写入操作，防止多线程竞争
    with excel_lock:
        try:
            # 检查文件是否存在，不存在则创建并写入标题
            if not os.path.exists(txt_path) or os.path.getsize(txt_path) == 0:
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write("账号----密码----登录状态----验证方式\n")
            
            # 检查账号是否已存在于文件中，如果存在需要更新
            update_needed = False
            existing_accounts = {}
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if i == 0:  # 跳过标题行
                            continue
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split('----')
                        if len(parts) >= 4:
                            acc_username = parts[0].strip()
                            if acc_username == username:
                                update_needed = True
                                break
            except:
                # 读取失败则视为文件为空或不需要更新
                pass
                
            # 如果账号已存在需要更新整个文件，否则直接追加
            if update_needed:
                # 读取所有账号信息
                existing_accounts = {}
                with open(txt_path, 'r', encoding='utf-8') as f:
                    # 跳过标题行
                    next(f, None)
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split('----')
                        if len(parts) >= 4:
                            acc_username = parts[0].strip()
                            acc_password = parts[1].strip()
                            acc_status = parts[2].strip()
                            acc_method = parts[3].strip()
                            existing_accounts[acc_username] = {
                                'password': acc_password,
                                'status': acc_status,
                                'method': acc_method
                            }
                
                # 更新当前账号
                existing_accounts[username] = {
                    'password': password,
                    'status': status,
                    'method': verification_method
                }
                
                # 重写文件
                with open(txt_path, 'w', encoding='utf-8') as f:
                    # 写入标题行
                    f.write("账号----密码----登录状态----验证方式\n")
                    
                    # 写入所有账号信息
                    for acc_username, acc_info in existing_accounts.items():
                        f.write(f"{acc_username}----{acc_info['password']}----{acc_info['status']}----{acc_info['method']}\n")
            else:
                # 直接追加当前账号
                with open(txt_path, 'a', encoding='utf-8') as f:
                    f.write(f"{username}----{password}----{status}----{verification_method}\n")
                    # 每次追加后确保文件立即写入磁盘
                    f.flush()
                    os.fsync(f.fileno())
            
            logger.info(f"账号 {username} 的登录结果已保存到 {os.path.abspath(txt_path)}")
            return True
            
        except Exception as e:
            logger.error(f"保存账号 {username} 的登录结果到文本文件失败: {str(e)}")
            return False


if __name__ == "__main__":
    import sys
    import os

    # 设置默认参数
    accounts_file = "conf/accounts.txt"
    output_dir = "login_results"
    delay = 0  # 每个账号的延迟
    max_concurrent = 10  # 最大线程数

    # 解析命令行参数
    if len(sys.argv) >= 2:
        accounts_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]
    if len(sys.argv) >= 4:
        try:
            delay = int(sys.argv[3])
        except ValueError:
            print(f"延迟参数必须是整数，使用默认值 {delay}")
    if len(sys.argv) >= 5:
        try:
            max_concurrent = int(sys.argv[4])
        except ValueError:
            print(f"并发任务数必须是整数，使用默认值 {max_concurrent}")

    # 检查账号文件是否存在
    if not os.path.exists(accounts_file):
        print(f"账号文件 {accounts_file} 不存在!")
        sys.exit(1)

    # 打印运行参数
    print(f"账号文件: {accounts_file}")
    print(f"输出目录: {output_dir}")
    print(f"任务间延迟: {delay}秒")
    print(f"最大并发数: {max_concurrent}")
    print(f"\n您可以随时打开'登录结果报告.txt'文件查看实时更新的登录结果")

    print("\n开始批量登录账号...")

    try:
        # 运行批量登录
        results = batch_login(accounts_file, output_dir, delay, max_concurrent)

        # 汇总结果
        print("\n登录结果汇总:")
        print(f"总计: {results['总计']} 个账号")
        print(f"成功或继续验证: {results['成功']} 个账号")
        print(f"失败: {results['失败']} 个账号")
        print(f"跳过: {results['跳过']} 个账号")
        print(f"成功率: {(results['成功'] / (results['总计'] - results['跳过']) * 100) if (results['总计'] - results['跳过']) > 0 else 0:.2f}%")

        # 输出文本报告路径
        txt_path = '登录结果报告.txt'
        if os.path.exists(txt_path):
            print(f"\n文本报告已保存到: {os.path.abspath(txt_path)}")
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序执行出错: {str(e)}")

    print("\n批量登录完成！")
