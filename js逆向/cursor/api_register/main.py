from cursor_register import register_cursor
import argparse
import sys
import os.path
import subprocess
from pathlib import Path

# 导入配置加载器
sys.path.append(str(Path(__file__).parent.parent))
from conf.config_loader import get_api_keys
from proxy_manager import get_proxy

# 获取配置的API密钥
DEFAULT_EMAIL_API_KEY, DEFAULT_CAPTCHA_API_KEY = get_api_keys()


def register_and_save(email_api_key, captcha_api_key, output_file=None, auto_refresh=False, use_proxy=True):
    """注册并保存结果到文件
    
    Args:
        email_api_key: 邮箱API密钥
        captcha_api_key: 验证码API密钥
        output_file: 输出文件路径，如果不指定则使用默认路径
        auto_refresh: 是否自动执行刷新
        use_proxy: 是否使用代理
    
    Returns:
        dict: 注册结果
    """
    # 获取代理配置
    proxy = get_proxy() if use_proxy else None
    if proxy:
        print(f"✅ 成功获取代理: {proxy['http']}")
    else:
        print("⚠️ 未使用代理或代理获取失败")

    # 调用原有的注册函数
    result = register_cursor(
        email_api_type="tempmail.lol",
        email_api_key=email_api_key,
        captcha_api_type="ez-captcha",
        captcha_api_key=captcha_api_key,
        proxy=proxy,
        use_mock=False
    )

    # 如果注册成功且指定了输出文件
    if result.get('success') and output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Email: {result.get('email')}\n")
                f.write(f"Password: {result.get('password')}\n")
                f.write(f"Token: {result.get('full_cookie')}\n")
                f.write(f"Access Token: {result.get('access_token')}\n")
                f.write(f"Refresh Token: {result.get('refresh_token')}\n")
            print(f"✅ 账号信息已保存到: {output_file}")

            # 添加额外的导出，方便刷新工具使用
            parent_dir = Path(output_file).parent.parent
            refresh_token_file = parent_dir / "token_for_refresh.txt"
            with open(refresh_token_file, 'w', encoding='utf-8') as f:
                f.write(f"{result.get('email')}\n")
                f.write(f"{result.get('full_cookie')}\n")
            print(f"✅ 刷新token信息已导出到: {refresh_token_file}")

            # 输出刷新命令
            refresh_cmd = f"python ../main.py all --email \"{result.get('email')}\" --token \"{result.get('full_cookie')}\""

            # 如果启用了自动刷新
            if auto_refresh:
                print(f"\n🔄 正在自动执行刷新...")
                print(f"🔹 执行命令: {refresh_cmd}")

                # 构建命令
                main_py_path = parent_dir / "main.py"
                cmd = [
                    sys.executable,
                    str(main_py_path),
                    "all",
                    "--email", result.get('email'),
                    "--token", result.get('full_cookie')
                ]

                # 执行命令
                try:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=str(parent_dir)
                    )

                    # 实时输出日志
                    while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            print(output.strip())

                    # 等待进程完成
                    returncode = process.poll()

                    if returncode == 0:
                        print("\n✅ 自动刷新完成！请重启Cursor客户端")
                    else:
                        print(f"\n⚠️ 自动刷新过程返回错误码: {returncode}")
                        print(f"🔹 您可以手动执行刷新命令: {refresh_cmd}")

                except Exception as e:
                    print(f"\n❌ 自动刷新过程发生错误: {str(e)}")
                    print(f"🔹 您可以手动执行刷新命令: {refresh_cmd}")
            else:
                print(f"🔹 您可以使用以下命令刷新Cursor客户端:")
                print(f"   {refresh_cmd}")

        except Exception as e:
            print(f"❌ 保存账号信息失败: {str(e)}")

    return result


if __name__ == "__main__":

    print("===== Cursor一键注册和刷新工具 =====")

    # 检查命令行参数
    parser = argparse.ArgumentParser(description="Cursor注册工具")
    parser.add_argument("--email-api-key", help="邮箱API密钥")
    parser.add_argument("--captcha-api-key", help="验证码API密钥")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--auto", action="store_true", help="自动执行刷新流程")
    parser.add_argument("--proxy", action="store_true", help="使用代理", default=True)
    parser.add_argument("--no-proxy", action="store_true", help="不使用代理")

    # 解析命令行参数
    args = parser.parse_args()

    # 如果设置了email_api_key参数，使用参数值
    if args.email_api_key:
        email_api_key = args.email_api_key
    else:
        # 检查默认值是否已设置
        if not DEFAULT_EMAIL_API_KEY:
            config_path = Path(__file__).parent.parent / 'conf' / 'conf.ini'
            print(f"\n⚠️ 未找到有效的API密钥，请配置您的API密钥")
            print(f"1. 打开配置文件: {config_path}")
            print("2. 在[api_keys]部分填入您的API密钥")
            print(f"3. 示例格式:\n[api_keys]\nemail_api_key = 您的邮箱API密钥\ncaptcha_api_key = 您的验证码API密钥")
            print("\n按任意键退出...")
            input()
            sys.exit(1)

        email_api_key = DEFAULT_EMAIL_API_KEY

    # 如果设置了captcha_api_key参数，使用参数值
    if args.captcha_api_key:
        captcha_api_key = args.captcha_api_key
    else:
        # 检查默认值是否已设置
        if not DEFAULT_CAPTCHA_API_KEY:
            config_path = Path(__file__).parent.parent / 'conf' / 'conf.ini'
            print(f"\n⚠️ 未找到有效的验证码API密钥，请配置您的API密钥")
            print(f"1. 打开配置文件: {config_path}")
            print("2. 在[api_keys]部分填入您的API密钥")
            print(f"3. 示例格式:\n[api_keys]\nemail_api_key = 您的邮箱API密钥\ncaptcha_api_key = 您的验证码API密钥")
            print("\n按任意键退出...")
            input()
            sys.exit(1)

        captcha_api_key = DEFAULT_CAPTCHA_API_KEY

    # 是否使用代理
    use_proxy = True

    # 是否自动刷新
    auto_refresh = False

    # 输出文件
    output_file = args.output

    # 设置默认输出文件
    if not output_file:
        # 获取当前目录下的.cursor_register目录
        current_dir = Path(__file__).parent
        output_dir = current_dir / ".cursor_register"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "cursor_account.txt"

    # 执行注册
    result = register_and_save(
        email_api_key=email_api_key,
        captcha_api_key=captcha_api_key,
        output_file=output_file,
        auto_refresh=auto_refresh,
        use_proxy=use_proxy
    )

    # 输出结果
    if result.get('success'):
        print("\n===== 注册成功 =====")
        print(f"邮箱: {result.get('email')}")
        print(f"密码: {result.get('password')}")
        print(f"Token: {result.get('full_cookie')}")

        if not auto_refresh:
            print("\n提示: 您可以使用 --auto 参数来自动执行刷新流程")
            print("例如: python main.py --email-api-key 您的邮箱API密钥 --captcha-api-key 您的验证码API密钥 --auto")

        # 没有命令行参数时，等待用户按键退出
        if len(sys.argv) <= 1:
            print("\n按任意键退出...")
            input()
        sys.exit(0)
    else:
        print("\n===== 注册失败 =====")
        print(f"原因: {result.get('message')}")

        # 没有命令行参数时，等待用户按键退出
        if len(sys.argv) <= 1:
            print("\n按任意键退出...")
            input()
        sys.exit(1)
