import time

import pandas as pd

from utils.login import auto_login
from utils.core_anwser import auto_save_answer

if __name__ == '__main__':
    # 读取 Excel 文件
    df = pd.read_excel('学习通刷课.xlsx')

    # 获取所需字段
    usernames = df['电话号码']
    pwds = df['密码/备注']
    courses = df['信息']
    statuses = df['状态']

    # 遍历每一行
    for idx, (name, pwd, course, status) in enumerate(zip(usernames, pwds, courses, statuses)):

        # # 打印测试数据
        print('正在刷题用户： ', name)
        print('密码： ', pwd)
        print('课程: ', course)
        try:
            # 判断状态是否为空
            if pd.isna(status) or status == '':
                # 自动登录
                cookie = auto_login(str(name).strip(), str(pwd).strip())
                if not cookie:
                    print('账号或密码错误! ')
                    continue

                # 自动提交答案
                msg = auto_save_answer(cookie, course)
                # print(msg)

                # 判断是否提交成功
                if '成功' in msg:
                    # 更新状态为 OK
                    df.at[idx, '状态'] = 'OK'
                    print("答案提交成功，状态更新为 OK")
                else:
                    print("答案提交失败! ")

        except Exception as e:
            print(e)
        print('----------------------')
    df.to_excel('学习通刷课.xlsx', index=False)
