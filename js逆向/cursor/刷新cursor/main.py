import os
import sqlite3
import logging
import platform
import time
from pathlib import Path
from argparse import ArgumentParser
import psutil  # 用于检测和关闭进程
import urllib.parse  # 用于解码 %3A%3A

# 配置日志
log_dir = Path.home() / ".cursor_auth"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# 获取 Cursor 存储目录
def get_cursor_storage_dir():
    system = platform.system().lower()
    home = Path.home()
    if system == "darwin":
        return home / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage"
    elif system == "windows":
        print('windows平台')
        return Path(os.getenv("APPDATA")) / "Cursor" / "User" / "globalStorage"
    else:  # Linux
        return home / ".config" / "Cursor" / "User" / "globalStorage"


# 检查 Cursor 进程
def check_and_close_cursor():
    system = platform.system().lower()
    cursor_process_names = ["Cursor", "Cursor.exe"] if system == "windows" else ["Cursor"]
    detected = False

    for proc in psutil.process_iter(['name', 'exe', 'pid']):
        try:
            proc_name = proc.info['name'].lower()
            proc_exe = proc.info['exe'] or "N/A"
            if any(cursor_name.lower() in proc_name for cursor_name in cursor_process_names):
                logger.warning(
                    f"检测到可能相关的进程: 名称={proc.info['name']}, PID={proc.info['pid']}, 路径={proc_exe}")
                detected = True
                # 可选：自动关闭 Cursor（取消注释以下代码）
                # try:
                #     proc.terminate()  # 尝试优雅终止
                #     proc.wait(timeout=5)  # 等待进程结束
                #     logger.info(f"已关闭进程: PID={proc.info['pid']}")
                # except psutil.Error as e:
                #     logger.error(f"关闭进程失败: PID={proc.info['pid']}, 错误={str(e)}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if detected:
        logger.warning("请确认所有 Cursor 相关进程已关闭（可在任务管理器或活动监视器中检查），然后重试")
        return True
    logger.info("未检测到 Cursor 进程")
    return False


# 解析服务端返回的 token
def parse_token(raw_token: str) -> str:
    try:
        # 解码 URL 编码的 %3A%3A 为 ::
        decoded_token = urllib.parse.unquote(raw_token)
        # 分割 user_id 和 JWT token
        parts = decoded_token.split("::")
        if len(parts) != 2:
            logger.error("Token 格式错误：缺少 :: 分隔符")
            return None
        jwt_token = parts[1]
        if not jwt_token.startswith("ey"):
            logger.error("无效的 JWT token 格式")
            return None
        return jwt_token
    except Exception as e:
        logger.error(f"解析 token 失败: {str(e)}")
        return None


# 刷新 Cursor 客户端 token
def refresh_cursor_token(email: str, raw_token: str) -> dict:
    logger.info("开始刷新 Cursor 客户端 token")
    try:
        refresh_token = raw_token
        # # 解析 token
        # refresh_token = parse_token(raw_token)
        # if not refresh_token:
        #     return {"success": False, "message": "无效的 token 格式"}

        # 确保存储目录存在
        cursor_storage_dir = get_cursor_storage_dir()
        cursor_storage_dir.mkdir(parents=True, exist_ok=True)
        state_file = cursor_storage_dir / "state.vscdb"

        # 检查 Cursor 是否运行
        if check_and_close_cursor():
            logger.info("建议关闭所有 Cursor 相关进程以避免数据库锁定")

        # 尝试写入数据库，带重试机制
        max_retries = 5  # 增加重试次数
        retry_delay = 2  # 增加重试间隔（秒）
        for attempt in range(max_retries):
            try:
                conn = sqlite3.connect(state_file, timeout=15)  # 增加超时时间
                cursor = conn.cursor()

                # 创建表（如果不存在）
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ItemTable (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                """)

                # 定义需要更新的键值对（与原 Electron 代码一致）
                updates = {
                    "cursorAuth/cachedSignUpType": "Auth_0",
                    "cursorAuth/signUpType": "Auth_0",
                    "cursorAuth/isLoggedIn": "true",
                    "cursorAuth/stripeMembershipType": "free_trial",
                    "cursorAuth/loginType": "Auth_0",
                    "cursorAuth/cachedLoginType": "Auth_0",
                    "cursorAuth/membershipType": "free_trial",
                    "cursorAuth/cachedMembershipType": "free_trial",
                    "cursorAuth/isAuthenticated": "true",
                    "cursorAuth/isAuthorized": "true",
                    "cursorAuth/isActivated": "true",
                    "cursorAuth/status": "active",
                    "cursorAuth/cachedEmail": email,
                    "cursorAuth/email": email,
                    "cursorAuth/username": email,
                    "cursorAuth/cachedUsername": email,
                    "cursorAuth/cachedAccessToken": refresh_token,
                    "cursorAuth/accessToken": refresh_token,
                    "cursorAuth/token": refresh_token,
                    "cursorAuth/refreshToken": refresh_token,
                    "cursorAuth/cachedRefreshToken": refresh_token,
                    "cursorAuth/idToken": refresh_token,
                    "cursorAuth/cachedIdToken": refresh_token
                }

                # 写入数据库
                for key, value in updates.items():
                    cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))

                # 提交事务
                conn.commit()
                logger.info("Cursor 客户端 token 刷新成功")
                logger.info("请重启 Cursor 客户端以应用新的认证信息")
                return {"success": True, "message": "Token 刷新成功，请重启 Cursor 客户端"}

            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    logger.warning(f"数据库锁定，重试 {attempt + 1}/{max_retries}")
                    time.sleep(retry_delay)
                    continue
                logger.error(f"数据库操作失败: {str(e)}")
                return {"success": False, "message": f"数据库操作失败: {str(e)}"}
            except Exception as e:
                logger.error(f"刷新 Cursor token 失败: {str(e)}", exc_info=True)
                return {"success": False, "message": f"刷新失败: {str(e)}"}
            finally:
                if 'conn' in locals():
                    conn.close()

        return {"success": False, "message": "数据库持续锁定，请关闭所有 Cursor 相关进程后重试"}

    except Exception as e:
        logger.error(f"刷新 Cursor token 失败: {str(e)}", exc_info=True)
        return {"success": False, "message": f"刷新失败: {str(e)}"}


# 主函数：命令行入口
def main():
    username = 'aminta78581@w0rli.awesome47.com'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoMHx1c2VyXzAxSlNHUzhYMFE3UDZGU1BTQUJFOE5XSlhNIiwidGltZSI6IjE3NDUzOTM4NTciLCJyYW5kb21uZXNzIjoiMWQ4M2MzNGItMjliMS00ZDY5IiwiZXhwIjoxNzUwNTc3ODU3LCJpc3MiOiJodHRwczovL2F1dGhlbnRpY2F0aW9uLmN1cnNvci5zaCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MiLCJhdWQiOiJodHRwczovL2N1cnNvci5jb20ifQ.E4x0eEJmVw5i1KizPqPAgvMgUvSVAat7_z8_vB7rojg'

    result = refresh_cursor_token(username, token)
    print(result["message"])


if __name__ == "__main__":
    main()
