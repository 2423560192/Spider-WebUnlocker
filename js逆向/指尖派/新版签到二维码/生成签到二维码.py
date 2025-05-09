#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import qrcode
import requests
from datetime import datetime
import os
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# 与项目中完全相同的密钥
ENCRYPT_KEY = "gNuRigdKZ4rMwKnpL2TXH4v51h33rRqt"
authorization_my = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdXRoIjp7InBhc3N3b3JkIjpudWxsLCJ1c2VybmFtZSI6InpqcDEwMDEwMDAwNTMxMjciLCJhdXRob3JpdGllcyI6W10sImFjY291bnROb25FeHBpcmVkIjp0cnVlLCJhY2NvdW50Tm9uTG9ja2VkIjp0cnVlLCJjcmVkZW50aWFsc05vbkV4cGlyZWQiOnRydWUsImVuYWJsZWQiOnRydWUsInVzZXJJZCI6MTAwMTAwMDA1MzEyNywib3BlbklkIjoib0ZPODI2U2lSRjlCbE5KVXo3bWxoMWptaE8wYyIsInNjaG9vbElkIjo2LCJiaW5kZWQiOjB9LCJqdGkiOiIwYTk4MDY0NS0yZjc0LTQ4NjUtODY5MC02YmZhZDg1N2ZhNjUiLCJpYXQiOjE3NDU1NjI4MTYsImV4cCI6MTc0NjE2NzYxNn0.6JH4rptGrubuvobBZZedZ2zRGN99YFjZRLXwJBPo9OE'
authorization = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdXRoIjp7InBhc3N3b3JkIjpudWxsLCJ1c2VybmFtZSI6InpqcDEwMDEwMDAwNTMxMjciLCJhdXRob3JpdGllcyI6W10sImFjY291bnROb25FeHBpcmVkIjp0cnVlLCJhY2NvdW50Tm9uTG9ja2VkIjp0cnVlLCJjcmVkZW50aWFsc05vbkV4cGlyZWQiOnRydWUsImVuYWJsZWQiOnRydWUsInVzZXJJZCI6MTAwMTAwMDA1MzEyNywib3BlbklkIjoib0ZPODI2U2lSRjlCbE5KVXo3bWxoMWptaE8wYyIsInNjaG9vbElkIjo2LCJiaW5kZWQiOjB9LCJqdGkiOiJmYTBlMDJjZC03MzViLTRkMTMtYTdlOS05ZGI4MTI2MWFhNTUiLCJpYXQiOjE3NDYzNDU0NDQsImV4cCI6MTc0Njk1MDI0NH0.Mr6ymcBFU_ex9Vd2LThA2CySRRN0EnZuzMdeF8kZM10'



def encrypt(text):
    """
    实现与项目完全一致的AES-ECB加密

    这与原项目中的encrypt函数完全对应:
    t.encrypt = function (e) {
        return null != e && e.length ? o.default.AES.encrypt(e, i, {
            mode: o.default.mode.ECB,
            padding: o.default.pad.Pkcs7
        }).toString() : ""
    }
    """
    if text is None or len(text) == 0:
        return ""

    # 转换密钥为UTF-8编码的字节
    key_bytes = ENCRYPT_KEY.encode('utf-8')

    # 创建AES-ECB加密器
    cipher = AES.new(key_bytes, AES.MODE_ECB)

    # 加密数据（使用PKCS7填充）
    text_bytes = text.encode('utf-8')
    padded_bytes = pad(text_bytes, AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_bytes)

    # 转换为Base64字符串，与CryptoJS.AES.encrypt输出格式一致
    return base64.b64encode(encrypted_bytes).decode('utf-8')


def get_user_sign(timestamp):
    """
    生成与小程序相同的User-Sign头
    """
    return encrypt(str(timestamp))


def get_sign_ids(activity_id, proxies):
    """获取活动的签到按钮列表"""
    url = "https://h5.wmzjp.com/zjp/act-activity-sign-button/listActivitySignButtons"

    # 生成当前时间戳和User-Sign头
    timestamp = int(time.time() * 1000)
    user_sign = get_user_sign(str(timestamp))

    headers = {
        'Host': 'h5.wmzjp.com',
        'accept': 'application/json, text/plain, */*',
        'xweb_xhr': '1',
        'authorization': authorization,
        'user-sign': user_sign,  # 添加User-Sign头
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
        response = requests.get(url, headers=headers, params=params, proxies=proxies)
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
    # 只替换非法字符（不包括路径分隔符）
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def create_qrcode(qr_data, size=180, output_file="sign_qrcode.png"):
    """
    严格按照微信小程序中的createQRCode函数逻辑实现

    参数:
    qr_data: 二维码数据内容
    size: 二维码尺寸，默认180
    output_file: 输出文件名
    """
    # 对应原代码: a = new s.default
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 对应原代码: a.data = e
    qr.add_data(qr_data)

    # 对应原代码: a.make()
    qr.make(fit=True)

    # 生成图像并调整大小
    img = qr.make_image(fill_color="black", back_color="white")
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
    # 构建二维码数据，完全保持与小程序一致
    qr_data = {
        "activityId": activity_id,
        "signId": sign_id,
        "buttonType": button_type,
        "isHide": 1,  # 添加isHide参数，与原始代码对应
        "type": button_type,  # 1表示签到/签退二维码
        "buttonName": button_name
    }

    # 如果是动态刷新二维码，添加时间戳和刷新时间
    if qrcode_type == 2:
        qr_data["currentTime"] = int(time.time() * 1000)  # 毫秒级时间戳
        qr_data["refreshTime"] = refresh_time  # 刷新时间(秒)

    # 将数据转换为JSON字符串
    qr_content = json.dumps(qr_data, ensure_ascii=False)
    print("原始二维码数据:", qr_content)

    # 加密数据 - 与小程序一致！
    encrypted_data = encrypt(qr_content)
    print("加密后的二维码数据:", encrypted_data)

    # 使用加密后的数据生成二维码
    file_path = create_qrcode(encrypted_data, 180, output_file)

    # 计算过期时间（仅用于返回）
    expiry_time = None
    if qrcode_type == 2 and "currentTime" in qr_data:
        expiry_time = datetime.fromtimestamp(
            (qr_data["currentTime"] / 1000) + refresh_time
        ).strftime("%Y-%m-%d %H:%M:%S")

    return file_path, expiry_time


def get_activity_name(activity_id, proxies):
    # 生成当前时间戳和User-Sign头
    timestamp = int(time.time() * 1000)
    user_sign = get_user_sign(str(timestamp))

    headers = {
        'Host': 'h5.wmzjp.com',
        'accept': 'application/json, text/plain, */*',
        'xweb_xhr': '1',
        'authorization': authorization,
        'user-sign': user_sign,  # 添加User-Sign头
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wxbd5a45d082ccacaa/34/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    params = {
        'id': activity_id,
    }

    response = requests.get('https://h5.wmzjp.com/zjp/act-activity/getActivityById', params=params, headers=headers,
                            proxies = proxies)
    data = response.json()
    if data.get("code") == 0 and "data" in data and "name" in data["data"]:
        return data["data"]["name"]
    else:
        return f"活动{activity_id}"


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


def main():
    # 自定义参数
    activity_id = 16272  # 活动ID
    sign_id = None  # 签到ID（如果为None则通过API获取）
    button_type = 1  # 1=签到, 2=签退
    qrcode_type = 2  # 必须设置为2（动态刷新二维码）
    refresh_time = 720000  # 刷新时间（秒）
    output_dir = 'qrcodes'

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 如果直接提供了签到ID
    if sign_id is not None:
        output_file = os.path.join(output_dir, f"sign_{activity_id}_{sign_id}.png")
        output_file, expiry_time = generate_sign_qrcode(
            activity_id,
            sign_id,
            button_type,
            "签到",  # 默认按钮名称
            qrcode_type,
            refresh_time,
            output_file
        )
        print(f"二维码已保存到: {output_file}")
        if expiry_time:
            print(f"二维码有效期至: {expiry_time}")
        return

    # 获取代理
    # proxies = get_proxy()
    # if not proxies:
    #     print("无法获取代理，将尝试直接请求")
    proxies = None

    # 获取签到按钮列表
    sign_buttons = get_sign_ids(activity_id, proxies)
    if not sign_buttons:
        print(f"未找到活动ID为 {activity_id} 的签到按钮")
        return

    print(f"找到 {len(sign_buttons)} 个签到按钮:")
    for i, button in enumerate(sign_buttons):
        button_id = button.get('id', '未知')
        button_name = button.get('name', '未命名')
        button_type = button.get('buttonType', 1)
        type_text = "签到" if button_type == 1 else "签退" if button_type == 2 else "未知类型"
        print(f"{i + 1}. ID: {button_id}, 名称: {button_name}, 类型: {type_text}")

    # 获取项目名
    name = get_activity_name(activity_id, proxies)
    # name = '测试'
    print(f"活动名称: {name}")

    # 创建项目目录
    project_dir = os.path.join(output_dir, sanitize_filename(name))
    os.makedirs(project_dir, exist_ok=True)

    for selected_button in sign_buttons:
        button_id = selected_button.get('id', '未知')
        button_name = selected_button.get('name', '签到')
        button_type = selected_button.get('buttonType', 1)

        filename = f"{name}_{button_name}.png"
        filename = sanitize_filename(filename)
        output_file = os.path.join(project_dir, filename)

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
        if expiry_time:
            print(f"二维码有效期至: {expiry_time}")


if __name__ == "__main__":
    main()
