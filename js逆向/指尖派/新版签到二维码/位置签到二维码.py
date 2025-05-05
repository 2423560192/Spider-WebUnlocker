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
authorization = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdXRoIjp7InBhc3N3b3JkIjpudWxsLCJ1c2VybmFtZSI6InpqcDEwMDEwMDAwOTc2NDQiLCJhdXRob3JpdGllcyI6W10sImFjY291bnROb25FeHBpcmVkIjp0cnVlLCJhY2NvdW50Tm9uTG9ja2VkIjp0cnVlLCJjcmVkZW50aWFsc05vbkV4cGlyZWQiOnRydWUsImVuYWJsZWQiOnRydWUsInVzZXJJZCI6MTAwMTAwMDA5NzY0NCwib3BlbklkIjoib0ZPODI2U293V1hTZ0tMb0FEc3lXYUtkMzlpcyIsInNjaG9vbElkIjo1LCJiaW5kZWQiOjB9LCJqdGkiOiJkNzg1MzRhZC04ZWQwLTQ0YTctOTIzOC00YWE5MjE1MmE0ZmQiLCJpYXQiOjE3NDU5MDg5NDYsImV4cCI6MTc0NjUxMzc0Nn0.eGZfgpvfc6E_jnhOPoHbyPwKLq_ZPhry7lNDluM03P4'


def encrypt(text):
    """
    实现与项目完全一致的AES-ECB加密
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


def get_sign_ids(activity_id, proxies=None):
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


def generate_location_sign_qrcode(activity_id, sign_id, latitude, longitude, distance=200,
                                  button_type=1, button_name="签到",
                                  qrcode_type=2, refresh_time=720000, output_file="location_sign_qrcode.png"):
    """
    生成位置签到或签退二维码

    参数:
    activity_id: 活动ID
    sign_id: 签到ID
    latitude: 纬度坐标
    longitude: 经度坐标
    distance: 有效签到距离(米)
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
        "isHide": 0,
        "type": '1',  # 类型固定为1
        "buttonName": button_name,
        "latitude": latitude,  # 添加纬度坐标
        "longitude": longitude,  # 添加经度坐标
        "distance": distance  # 添加有效距离范围(米)
    }

    # 如果是动态刷新二维码，添加时间戳和刷新时间
    if qrcode_type == 2:
        qr_data["currentTime"] = int(time.time() * 1000)  # 毫秒级时间戳
        qr_data["refreshTime"] = refresh_time  # 刷新时间(秒)

    # 将数据转换为JSON字符串
    qr_content = json.dumps(qr_data, ensure_ascii=False)
    print(f"\n位置{'签到' if button_type == 1 else '签退'}二维码原始数据:", qr_content)

    # 加密数据 - 与小程序一致！
    encrypted_data = encrypt(qr_content)
    print("加密后的二维码数据:", encrypted_data[:50] + "...")

    # 使用加密后的数据生成二维码
    file_path = create_qrcode(encrypted_data, 180, output_file)

    # 计算过期时间（仅用于返回）
    expiry_time = None
    if qrcode_type == 2 and "currentTime" in qr_data:
        expiry_time = datetime.fromtimestamp(
            (qr_data["currentTime"] / 1000) + refresh_time
        ).strftime("%Y-%m-%d %H:%M:%S")

    return file_path, expiry_time


def get_activity_name(activity_id, proxies=None):
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

    try:
        response = requests.get('https://h5.wmzjp.com/zjp/act-activity/getActivityById', params=params, headers=headers,
                                proxies=proxies)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 0 and "data" in data and "name" in data["data"]:
            return data["data"]["name"]
    except Exception as e:
        print(f"获取活动名称失败: {e}")

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


def get_location_by_ip():
    """使用IP获取大致位置"""
    try:
        response = requests.get("https://ipapi.co/json/", timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "city": data.get("city"),
            "region": data.get("region")
        }
    except Exception as e:
        print(f"通过IP获取位置失败: {e}")
        return None


def create_location_qrcode(activity_id, sign_id, output_dir="qrcodes"):
    """
    直接生成位置签到或签退二维码

    参数:
    activity_id: 活动ID
    sign_id: 签到ID
    output_dir: 输出目录
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 选择签到类型
    print("\n=== 创建位置二维码 ===")
    print("1. 签到二维码")
    print("2. 签退二维码")
    button_type_input = input("请选择类型 (1/2): ").strip() or "1"
    button_type = int(button_type_input) if button_type_input in ["1", "2"] else 1
    button_name = "签到" if button_type == 1 else "签退"

    # 选择位置获取方式
    print(f"\n=== 设置位置{button_name}坐标 ===")
    print("1. 手动输入经纬度")
    print("2. 尝试通过IP获取当前位置")
    location_method = input("请选择获取位置方式 (1/2): ").strip() or "1"

    default_latitude = 29.01150  # 默认纬度坐标
    default_longitude = 106.69707  # 默认经度坐标

    if location_method == "2":
        print("正在尝试通过IP获取位置...")
        location = get_location_by_ip()
        if location and location.get("latitude") and location.get("longitude"):
            default_latitude = location.get("latitude")
            default_longitude = location.get("longitude")
            print(f"获取成功! 位置: {location.get('city', '')}, {location.get('region', '')}")
            print(f"坐标: 纬度{default_latitude}, 经度{default_longitude}")
        else:
            print("通过IP获取位置失败，将使用默认坐标")

    # 无论使用哪种方式获取初始坐标，都允许用户手动修改
    print("\n请确认或修改位置坐标(直接回车使用显示值):")

    try:
        latitude_input = input(f"纬度坐标 (默认: {default_latitude}): ")
        latitude = float(latitude_input) if latitude_input.strip() else default_latitude

        longitude_input = input(f"经度坐标 (默认: {default_longitude}): ")
        longitude = float(longitude_input) if longitude_input.strip() else default_longitude
    except ValueError:
        print("输入格式错误，将使用默认值")
        latitude = default_latitude
        longitude = default_longitude

    # 设置有效距离范围
    print("\n请设置有效距离范围:")
    print("推荐值: 200米(教室), 500米(校园), 1000米(社区), 5000米(城市)")
    print("注意: 距离越大对位置精度要求越低，设置较大值可提高签到成功率")

    try:
        default_distance = 1000  # 默认1000米
        distance_input = input(f"有效距离范围(米) (默认: {default_distance}): ")
        distance = int(distance_input) if distance_input.strip() else default_distance

        # 提供一些安全提示，如果距离设置得很小
        if distance < 200:
            confirm = input("警告: 距离设置较小(<200米)可能导致部分用户无法签到。是否继续?(y/n): ").lower()
            if confirm != 'y':
                distance = 200
                print(f"已将距离调整为安全值: {distance}米")
    except ValueError:
        print("输入格式错误，将使用默认值")
        distance = 1000

    # 设置刷新时间
    print("\n请设置二维码刷新时间:")
    default_refresh_time = 720000  # 默认刷新时间(秒)
    try:
        refresh_time_input = input(f"刷新时间(秒) (默认: {default_refresh_time / 60:.1f}分钟): ")
        refresh_time = int(refresh_time_input) if refresh_time_input.strip() else default_refresh_time
    except ValueError:
        print("输入格式错误，将使用默认值")
        refresh_time = default_refresh_time

    # 获取活动名称
    try:
        name = get_activity_name(activity_id)
    except:
        name = f"活动{activity_id}"

    name = sanitize_filename(name)

    new_path = os.path.join(output_dir, name)

    os.makedirs(new_path, exist_ok=True)

    # 创建文件名
    if sign_id:
        filename = f"{button_name}_位置{button_name}_{latitude}_{longitude}_{distance}米.png"
    else:
        sign_id = int(activity_id) * 100 + 1  # 默认签到ID
        filename = f"{button_name}_位置{button_name}_默认ID_{latitude}_{longitude}_{distance}米.png"

    output_file = os.path.join(new_path, filename)

    # 生成位置签到二维码
    output_file, expiry_time = generate_location_sign_qrcode(
        activity_id,
        sign_id,
        latitude,
        longitude,
        distance,
        button_type,  # 签到类型 (1=签到, 2=签退)
        button_name,
        2,  # 动态刷新二维码
        refresh_time,  # 刷新时间(秒)
        output_file
    )

    print(f"\n位置{button_name}二维码已保存到: {output_file}")
    print(f"有效距离: {distance}米")
    print(f"坐标: 纬度{latitude}, 经度{longitude}")
    if expiry_time:
        print(f"二维码有效期至: {expiry_time}")
    print("\n提示: 请将此二维码发给需要{button_name}的用户扫描")
    print(f"      用户需在距离设定位置{distance}米范围内才能成功{button_name}")

    return output_file


def create_location_qrcodes_batch(activity_id, sign_buttons, output_dir="qrcodes", batch_distance=None):
    """批量生成位置签到/签退二维码"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取活动名称
    try:
        activity_name = get_activity_name(activity_id)
    except:
        activity_name = f"活动{activity_id}"

    # 询问是否使用相同的位置坐标和距离
    print("\n=== 批量生成位置二维码 ===")
    print("找到以下签到/签退按钮:")

    for i, button in enumerate(sign_buttons):
        button_id = button.get('id', '未知')
        button_name = button.get('name', '未命名')
        button_type = button.get('buttonType', 1)
        type_text = "签到" if button_type == 1 else "签退" if button_type == 2 else "未知类型"
        print(f"{i + 1}. ID: {button_id}, 名称: {button_name}, 类型: {type_text}")

    print("\n请选择批量生成方式:")
    same_location = input("是否对所有按钮使用相同的位置坐标和距离? (y/n): ").lower() == 'y'

    # 获取共享位置信息
    default_latitude = 30.548
    default_longitude = 104.052
    default_distance = 1000

    if same_location:
        # 选择位置获取方式
        print("\n=== 设置共享位置坐标 ===")
        print("1. 手动输入经纬度")
        print("2. 尝试通过IP获取当前位置")
        location_method = input("请选择获取位置方式 (1/2): ").strip() or "1"

        if location_method == "2":
            print("正在尝试通过IP获取位置...")
            location = get_location_by_ip()
            if location and location.get("latitude") and location.get("longitude"):
                default_latitude = location.get("latitude")
                default_longitude = location.get("longitude")
                print(f"获取成功! 位置: {location.get('city', '')}, {location.get('region', '')}")
                print(f"坐标: 纬度{default_latitude}, 经度{default_longitude}")
            else:
                print("通过IP获取位置失败，将使用默认坐标")

        print("\n请确认或修改位置坐标(直接回车使用显示值):")

        try:
            latitude_input = input(f"纬度坐标 (默认: {default_latitude}): ")
            shared_latitude = float(latitude_input) if latitude_input.strip() else default_latitude

            longitude_input = input(f"经度坐标 (默认: {default_longitude}): ")
            shared_longitude = float(longitude_input) if longitude_input.strip() else default_longitude
        except ValueError:
            print("输入格式错误，将使用默认值")
            shared_latitude = default_latitude
            shared_longitude = default_longitude

        # 设置有效距离范围
        print("\n请设置有效距离范围:")
        print("推荐值: 200米(教室), 500米(校园), 1000米(社区), 5000米(城市)")

        try:
            distance_input = input(f"有效距离范围(米) (默认: {default_distance}): ")
            shared_distance = int(distance_input) if distance_input.strip() else default_distance
        except ValueError:
            print("输入格式错误，将使用默认值")
            shared_distance = default_distance

    # 设置刷新时间
    print("\n请设置二维码刷新时间:")
    default_refresh_time = 720000  # 默认刷新时间(秒)
    try:
        refresh_time_input = input(f"刷新时间(秒) (默认: {default_refresh_time / 60:.1f}分钟): ")
        refresh_time = int(refresh_time_input) if refresh_time_input.strip() else default_refresh_time
    except ValueError:
        print("输入格式错误，将使用默认值")
        refresh_time = default_refresh_time

    # 开始批量生成二维码
    generated_files = []

    for i, button in enumerate(sign_buttons):
        button_id = button.get('id', '未知')
        button_name = button.get('name', '未命名')
        button_type = button.get('buttonType', 1)
        type_text = "签到" if button_type == 1 else "签退" if button_type == 2 else "未知类型"

        print(f"\n[{i + 1}/{len(sign_buttons)}] 正在生成{type_text}二维码: {button_name}...")

        if same_location:
            # 使用共享位置信息
            latitude = shared_latitude
            longitude = shared_longitude
            distance = shared_distance
        else:
            # 为每个按钮单独设置位置
            print(f"\n=== 为 {button_name} ({type_text}) 设置位置 ===")
            # 选择位置获取方式
            print("1. 手动输入经纬度")
            print("2. 尝试通过IP获取当前位置")
            location_method = input("请选择获取位置方式 (1/2): ").strip() or "1"

            if location_method == "2":
                print("正在尝试通过IP获取位置...")
                location = get_location_by_ip()
                if location and location.get("latitude") and location.get("longitude"):
                    default_latitude = location.get("latitude")
                    default_longitude = location.get("longitude")
                    print(f"获取成功! 位置: {location.get('city', '')}, {location.get('region', '')}")
                    print(f"坐标: 纬度{default_latitude}, 经度{default_longitude}")
                else:
                    print("通过IP获取位置失败，将使用默认坐标")

            try:
                latitude_input = input(f"纬度坐标 (默认: {default_latitude}): ")
                latitude = float(latitude_input) if latitude_input.strip() else default_latitude

                longitude_input = input(f"经度坐标 (默认: {default_longitude}): ")
                longitude = float(longitude_input) if longitude_input.strip() else default_longitude
            except ValueError:
                print("输入格式错误，将使用默认值")
                latitude = default_latitude
                longitude = default_longitude

            # 设置有效距离范围
            try:
                distance_input = input(f"有效距离范围(米) (默认: {default_distance}): ")
                distance = int(distance_input) if distance_input.strip() else default_distance
            except ValueError:
                print("输入格式错误，将使用默认值")
                distance = default_distance

        # 创建文件名
        filename = f"{activity_name}_{button_name}_{type_text}_{latitude}_{longitude}_{distance}米.png"
        filename = sanitize_filename(filename)
        output_file = os.path.join(output_dir, filename)

        # 生成位置签到/签退二维码
        output_file, expiry_time = generate_location_sign_qrcode(
            activity_id,
            button_id,
            latitude,
            longitude,
            distance,
            button_type,  # 签到类型 (1=签到, 2=签退)
            button_name,
            2,  # 动态刷新二维码
            refresh_time,  # 刷新时间(秒)
            output_file
        )

        print(f"\n{type_text}二维码已保存到: {output_file}")
        print(f"有效距离: {distance}米")
        print(f"坐标: 纬度{latitude}, 经度{longitude}")
        if expiry_time:
            print(f"二维码有效期至: {expiry_time}")

        generated_files.append(output_file)

    print(f"\n成功批量生成 {len(generated_files)} 个位置二维码!")
    return generated_files


def main():
    # 自定义参数
    activity_id = 15519  # 活动ID
    sign_id = None  # 签到ID（如果为None则通过API获取）

    # 提示用户选择操作
    print("=== 指尖派二维码生成工具 ===")
    print("1. 生成位置签到/签退二维码")
    print("2. 获取活动所有签到按钮信息")
    print("3. 批量生成位置签到/签退二维码")

    choice = input("请选择操作 (1/2/3): ").strip() or "1"

    # 处理不同选择
    if choice == "1":
        # 位置签到二维码
        activity_id = input(f"请输入活动ID (默认: {activity_id}): ").strip() or activity_id
        sign_id_input = input("请输入签到ID (留空自动生成): ").strip()
        sign_id = int(sign_id_input) if sign_id_input else None

        create_location_qrcode(activity_id, sign_id)

    elif choice == "2":

        # 获取活动所有按钮信息

        activity_id = input(f"请输入活动ID (默认: {activity_id}): ").strip() or activity_id

        # 获取代理

        proxies = None

        try:

            proxies = get_proxy()

        except:

            print("无法获取代理，将尝试直接请求")

        # 获取签到按钮列表

        sign_buttons = get_sign_ids(activity_id, proxies)

        if not sign_buttons:

            print(f"未找到活动ID为 {activity_id} 的签到按钮")

            create_button = input("是否要创建一个默认的签到按钮? (y/n): ").lower() == 'y'

            if create_button:
                sign_id = int(activity_id) * 100 + 1

                print(f"将使用默认签到ID: {sign_id}")

                create_location_qrcode(activity_id, sign_id)

            return

        # 获取活动名称

        try:

            activity_name = get_activity_name(activity_id)

            print(f"\n活动名称: {activity_name}")

        except:

            print(f"\n活动ID: {activity_id}")

        print(f"找到 {len(sign_buttons)} 个签到/签退按钮:")

        for i, button in enumerate(sign_buttons):
            button_id = button.get('id', '未知')

            button_name = button.get('name', '未命名')

            button_type = button.get('buttonType', 1)

            status = button.get('status', 0)

            type_text = "签到" if button_type == 1 else "签退" if button_type == 2 else "未知类型"

            status_text = "已开启" if status == 1 else "已停止" if status == 2 else "未知状态"

            print(f"{i + 1}. ID: {button_id}, 名称: {button_name}, 类型: {type_text}, 状态: {status_text}")

        # 询问是否生成一个按钮的二维码

        create_one = input("\n是否要为其中一个按钮生成位置二维码? (y/n): ").lower() == 'y'

        if create_one:

            button_index = input(f"请选择要生成位置二维码的按钮 (1-{len(sign_buttons)}): ").strip()

            try:

                index = int(button_index) - 1

                if 0 <= index < len(sign_buttons):

                    selected_button = sign_buttons[index]

                    button_id = selected_button.get('id', '未知')

                    create_location_qrcode(activity_id, button_id)

                else:

                    print("选择无效，将使用第一个按钮")

                    selected_button = sign_buttons[0]

                    button_id = selected_button.get('id', '未知')

                    create_location_qrcode(activity_id, button_id)

            except:

                print("输入无效，将使用第一个按钮")

                selected_button = sign_buttons[0]

                button_id = selected_button.get('id', '未知')

                create_location_qrcode(activity_id, button_id)


    elif choice == "3":

        # 批量生成位置签到/签退二维码

        activity_id = input(f"请输入活动ID (默认: {activity_id}): ").strip() or activity_id

        output_dir = 'qrcodes'

        # 确保输出目录存在

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 获取代理

        proxies = None

        try:

            proxies = get_proxy()

        except:

            print("无法获取代理，将尝试直接请求")

        # 获取签到按钮列表

        sign_buttons = get_sign_ids(activity_id, proxies)

        if not sign_buttons:

            print(f"未找到活动ID为 {activity_id} 的签到按钮")

            create_button = input("是否要创建一个默认的签到按钮? (y/n): ").lower() == 'y'

            if create_button:
                sign_id = int(activity_id) * 100 + 1

                print(f"将使用默认签到ID: {sign_id}")

                create_location_qrcode(activity_id, sign_id)

            return

        # 批量生成

        create_location_qrcodes_batch(activity_id, sign_buttons, output_dir)


    else:

        print("选择无效，默认生成位置签到二维码")

        activity_id = input(f"请输入活动ID (默认: {activity_id}): ").strip() or activity_id

        create_location_qrcode(activity_id, sign_id)


if __name__ == "__main__":
    # 欢迎信息

    print("\n===================================================")

    print("   指尖派位置签到/签退二维码生成工具")

    print("===================================================")

    print("本工具可用于生成包含位置信息的签到/签退二维码")

    print("用户必须在指定位置附近才能成功签到/签退")

    print("注意: 请合理设置距离范围，过小可能导致无法签到")

    print("===================================================\n")

    main()

    print("\n感谢使用本工具!")
