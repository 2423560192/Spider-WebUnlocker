import subprocess

result_1 = subprocess.check_output("adb forward tcp:27042 tcp:27042", shell=True, text=True,
                                   stderr=subprocess.STDOUT, encoding='gbk')
result_2 = subprocess.check_output("adb forward tcp:27043 tcp:27043", text=True,
                                   stderr=subprocess.STDOUT, shell=True, encoding='gbk')
