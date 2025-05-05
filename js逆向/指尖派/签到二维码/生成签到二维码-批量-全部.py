
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import time
import qrcode
import requests
from datetime import datetime, date
import os
import re
import pandas as pd

authorization = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdXRoIjp7InBhc3N3b3JkIjpudWxsLCJ1c2VybmFtZSI6InpqcDEwMDEwMDAwOTc2NDQiLCJhdXRob3JpdGllcyI6W10sImFjY291bnROb25FeHBpcmVkIjp0cnVlLCJhY2NvdW50Tm9uTG9ja2VkIjp0cnVlLCJjcmVkZW50aWFsc05vbkV4cGlyZWQiOnRydWUsImVuYWJsZWQiOnRydWUsInVzZXJJZCI6MTAwMTAwMDA5NzY0NCwib3BlbklkIjoib0ZPODI2U293V1hTZ0tMb0FEc3lXYUtkMzlpcyIsInNjaG9vbElkIjo1LCJiaW5kZWQiOjB9LCJqdGkiOiJjY2ZjZWVlNC1iYmE0LTQ3ZDktYTNiMC05MWY1ZjFjNDVlMTUiLCJpYXQiOjE3NDU1NjAwMDksImV4cCI6MTc0NjE2NDgwOX0.TsNN9uJFnY4TBogdq4BHBAtw5k1p7aN9UZsVj3rU0Kw'

def get_proxy():
    """从代理API获取代理地址"""
    proxy_api = 'http://api2.xkdaili.com/tools/XApi.ashx?apikey=XK69862370B1CA650629&qty=1&format=txt&split=0&sign=87a269171ead05ba5185eba8eb5a162a&time=3'
    try:
        response = requests.get(proxy_api, timeout=10)
        response.raise_for_status()
        proxy_address = response.text.strip()
        if not proxy_address:
            print("代理API返回空地址")
            return None
        print(f"成功获取代理地址：{proxy_address}")
        return {'http': f'http://{proxy_address}', 'https': f'http://{proxy_address}'}
    except Exception as e:
        print(f"获取代理失败：{e}")
        return None

def get_sign_ids(activity_id, proxies=None):
    """获取活动的签到按钮列表"""
    url = "https://h5.wmzjp.com/act-activity-sign-button/listActivitySignButtons"
    headers = {
        'Host': 'h5.wmzjp.com',
        'accept': 'application/json, text/plain, */*',
        'xweb_xhr': '1',
        'authorization': authorization,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wxbd5a45d082ccacaa/34/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    params = {
        "activityId": activity_id
    }

    try:
        response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get("code") == 0 and "data" in data and "list" in data["data"]:
            return data["data"]["list"]
        else:
            print(f"获取签到ID失败: {data.get('message', '未知错误')}")
    except Exception as e:
        print(f"请求失败: {e}")

    return []

def sanitize_filename(filename):
    """清理文件名中的非法字符"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def create_qrcode(qr_data, size=180, output_file="sign_qrcode.png"):
    """
    严格按照微信小程序中的createQRCode函数逻辑实现

    参数:
    qr_data: 二维码数据内容
    size: 二维码尺寸，默认180
    output_file: 输出文件名
    """
    # 初始化二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 添加数据
    qr.add_data(qr_data)

    # 生成二维码
    qr.make(fit=True)

    # 创建图像
    img = qr.make_image(fill_color="black", back_color="white")

    # 调整尺寸
    img = img.resize((size, size))

    # 保存图像
    img.save(output_file)

    return output_file

def generate_sign_qrcode(activity_id, sign_id, button_type=1, button_name="签到",
                         qrcode_type=2, refresh_time=3600, output_file="sign_qrcode.png"):
    """
    生成活动签到二维码

    参数:
    activity_id: 活动ID
    sign_id: 签到ID
    button_type: 按钮类型, 1=签到, 2=签退
    button_name: 按钮名称
    qrcode_type: 二维码类型, 1=固定二维码, 2=刷新二维码
    refresh_time: 刷新时间(秒)
    output_file: 输出文件名
    """
    # 构建二维码数据
    qr_data = {
        "activityId": activity_id,
        "signId": sign_id,
        "buttonType": button_type,
        "type": 1,  # 1表示签到/签退二维码
        "buttonName": button_name
    }

    # 添加时间戳和刷新时间
    qr_data["currentTime"] = int(time.time() * 1000)  # 毫秒级时间戳
    qr_data["refreshTime"] = refresh_time  # 刷新时间(秒)

    # 转换为JSON字符串
    qr_content = json.dumps(qr_data, ensure_ascii=False)
    print("二维码数据:", qr_content)

    # 生成二维码
    file_path = create_qrcode(qr_content, 180, output_file)

    # 计算过期时间
    expiry_time = datetime.fromtimestamp(
        (qr_data["currentTime"] / 1000) + refresh_time
    ).strftime("%Y-%m-%d %H:%M:%S")

    return file_path, expiry_time

def main():
    # 自定义参数
    excel_file = r'../活动/待开始的活动.xlsx'  # Excel文件路径
    output_dir = 'qrcodes'  # 输出目录
    qrcode_type = 2  # 动态刷新二维码
    refresh_time = 3600 * 24 * 30  # 刷新时间（秒），约200小时
    button_type = 1  # 1=签到, 2=签退

    proxies = None

    # 检查Excel文件是否存在
    if not os.path.exists(excel_file):
        print(f"Excel文件 {excel_file} 不存在，请先运行活动获取脚本。")
        return

    # 读取Excel文件
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        if df.empty:
            print("Excel文件中没有数据。")
            return
    except Exception as e:
        print(f"读取Excel文件失败：{e}")
        return


    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历今天的活动
    for index, row in df.iterrows():

        people = row['总人数']


        if int(people) < 50:
            continue

        activity_id = row['ID']
        activity_name = row['活动名称']

        # 清理活动名称以用作目录名
        safe_activity_name = sanitize_filename(activity_name)
        activity_dir = os.path.join(output_dir, safe_activity_name)

        # 检查活动是否已处理
        if os.path.exists(activity_dir):
            print(f"活动 {activity_name} 已处理，跳过。")
            continue

        # 创建活动目录
        os.makedirs(activity_dir, exist_ok=True)

        print(f"正在处理活动：{activity_name} (ID: {activity_id})")

        # 获取签到按钮列表
        sign_buttons = get_sign_ids(activity_id, proxies=proxies)
        if not sign_buttons:
            print(f"未找到活动ID为 {activity_id} 的签到按钮")
            continue

        print(f"找到 {len(sign_buttons)} 个签到按钮:")
        for i, button in enumerate(sign_buttons):
            button_id = button.get('id', '未知')
            button_name = button.get('name', '签到')
            button_type = button.get('buttonType', 1)
            type_text = "签到" if button_type == 1 else "签退" if button_type == 2 else "未知类型"
            print(f"{i + 1}. ID: {button_id}, 名称: {button_name}, 类型: {type_text}")

        # 为每个签到按钮生成二维码
        for button in sign_buttons:
            button_id = button.get('id', '未知')
            button_name = button.get('name', '签到')
            button_type = button.get('buttonType', 1)

            # 生成文件名
            filename = f"{safe_activity_name}_{button_name}.png"
            filename = sanitize_filename(filename)
            output_file = os.path.join(activity_dir, filename)

            try:
                # 生成二维码
                output_file, expiry_time = generate_sign_qrcode(
                    activity_id,
                    button_id,
                    button_type,
                    button_name,
                    qrcode_type,
                    refresh_time,
                    output_file
                )
                print(f"二维码已保存到: {output_file}")
                print(f"二维码有效期至: {expiry_time}")
            except Exception as e:
                print(f"生成二维码失败 (活动: {activity_name}, 按钮: {button_name})：{e}")

        # 活动间延迟
        time.sleep(random.randint(1 , 4))

if __name__ == "__main__":
    main()