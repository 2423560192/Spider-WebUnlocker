"""
实时监控服务器某个后台服务日志
"""
import paramiko
import time


def tail_journalctl_log(host, username, password, service_name):
    # 连接到服务器
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接服务器
    client.connect(host, username=username, password=password)

    # 使用 journalctl 命令来实时获取日志
    command = f"journalctl -u {service_name} -f"
    stdin, stdout, stderr = client.exec_command(command)

    # 实时输出日志内容
    while True:
        line = stdout.readline()
        if not line:
            time.sleep(0.1)  # 如果没有新内容，稍等片刻
            continue
        print(line, end="")


if __name__ == "__main__":
    # 服务器连接信息
    host = "119.29.5.196"  # 替换为你的服务器 IP
    username = "root"  # 替换为你的服务器用户名
    password = "jd123123."  # 替换为你的服务器密码
    service_name = "miansui.service"  # 替换为你的服务名

    # 启动日志监控
    tail_journalctl_log(host, username, password, service_name)
