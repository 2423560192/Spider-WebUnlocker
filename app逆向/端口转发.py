import subprocess

# 执行 adb 命令来转发端口，并捕获输出
try:
    result_1 = subprocess.check_output("adb forward tcp:27042 tcp:27042", shell=True, text=True,
                                       stderr=subprocess.STDOUT, encoding='gbk')
    result_2 = subprocess.check_output("adb forward tcp:27043 tcp:27043", text=True,
                                       stderr=subprocess.STDOUT, shell=True, encoding='gbk')
    print(f"第一个命令的输出: {result_1}")
    print(f"第二个命令的输出: {result_2}")
except subprocess.CalledProcessError as e:
    print(f"发生错误: {e}")
