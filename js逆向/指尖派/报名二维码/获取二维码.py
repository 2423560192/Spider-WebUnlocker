import qrcode
import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import time
from datetime import datetime

# 与项目中完全相同的密钥
ENCRYPT_KEY = "gNuRigdKZ4rMwKnpL2TXH4v51h33rRqt"


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


def create_qrcode(data, filename='qrcode.png', size=150, error_correction=qrcode.constants.ERROR_CORRECT_M):
    """
    根据传入的字符串生成二维码，并保存为图片文件。

    :param data: 要编码的字符串（比如一个链接或加密数据）
    :param filename: 生成的图片文件名
    :param size: 图片尺寸（像素）
    :param error_correction: 错误纠正级别
    """
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,  # 控制二维码的大小，1 是最小的
        error_correction=error_correction,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    # 创建图像
    img = qr.make_image(fill_color="black", back_color="white")

    # 修改图像尺寸
    img = img.resize((size, size))

    # 确保目录存在
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)

    # 保存图像
    img.save(filename)
    print(f"二维码已保存为: {filename}")
    return filename


def create_report_qrcode(activity_id, output_file="report_qrcode.png", size=150):
    """
    创建现场报道二维码

    :param activity_id: 活动ID
    :param output_file: 输出文件名
    :param size: 图片尺寸
    """
    # 现场报道二维码使用的是URL格式
    base_url = "https://web.wmzjp.com/QRCode/report"
    full_url = f"{base_url}?type=2&activityId={activity_id}"

    print(f"生成现场报道二维码，URL: {full_url}")

    # 使用高纠错级别，增强可读性
    return create_qrcode(
        full_url,
        filename=output_file,
        size=size,
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )


def create_sign_qrcode(activity_id, sign_id, button_type=1, button_name="签到",
                       qrcode_type=2, refresh_time=720000, output_file="sign_qrcode.png", size=180):
    """
    生成活动签到二维码，使用加密方式

    :param activity_id: 活动ID
    :param sign_id: 签到ID
    :param button_type: 按钮类型, 1=签到, 2=签退
    :param button_name: 按钮名称
    :param qrcode_type: 二维码类型, 1=固定二维码, 2=刷新二维码
    :param refresh_time: 刷新时间(秒)
    :param output_file: 输出文件名
    :param size: 图片尺寸
    """
    # 构建二维码数据
    qr_data = {
        "activityId": activity_id,
        "signId": sign_id,
        "buttonType": button_type,
        "isHide": False,
        "type": 1,
        "buttonName": button_name
    }

    # 如果是动态刷新二维码，添加时间戳和刷新时间
    if qrcode_type == 2:
        qr_data["currentTime"] = int(time.time() * 1000)  # 毫秒级时间戳
        qr_data["refreshTime"] = refresh_time  # 刷新时间(秒)

    # 将数据转换为JSON字符串
    qr_content = json.dumps(qr_data, ensure_ascii=False)
    print(f"签到二维码原始数据: {qr_content}")

    # 加密数据
    encrypted_data = encrypt(qr_content)
    print(f"签到二维码加密数据: {encrypted_data[:30]}...（已截断）")

    # 计算过期时间
    expiry_time = None
    if qrcode_type == 2 and "currentTime" in qr_data:
        expiry_time = datetime.fromtimestamp(
            (qr_data["currentTime"] / 1000) + refresh_time
        ).strftime("%Y-%m-%d %H:%M:%S")
        print(f"二维码有效期至: {expiry_time}")

    # 使用加密后的数据生成二维码
    return create_qrcode(
        encrypted_data,
        filename=output_file,
        size=size,
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )


def generate_all_qrcodes(activity_id, output_dir="qrcodes", sign_id=None):
    """
    为指定活动生成所有类型的二维码

    :param activity_id: 活动ID
    :param output_dir: 输出目录
    :param sign_id: 签到ID(可选)
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 为活动创建子目录
    activity_dir = os.path.join(output_dir, f"活动_{activity_id}")
    os.makedirs(activity_dir, exist_ok=True)

    # 生成现场报道二维码
    report_file = os.path.join(activity_dir, f"现场报道_{activity_id}.png")
    create_report_qrcode(activity_id, report_file)

    # 如果提供了签到ID，生成签到二维码
    if sign_id:
        sign_file = os.path.join(activity_dir, f"签到_{activity_id}_{sign_id}.png")
        create_sign_qrcode(activity_id, sign_id, button_type=1, button_name="签到", output_file=sign_file)

        signout_file = os.path.join(activity_dir, f"签退_{activity_id}_{sign_id}.png")
        create_sign_qrcode(activity_id, sign_id, button_type=2, button_name="签退", output_file=signout_file)
    else:
        # 使用默认签到ID（通常是活动ID*100+1）
        default_sign_id = int(activity_id) * 100 + 1
        default_signout_id = int(activity_id) * 100 + 2

        sign_file = os.path.join(activity_dir, f"默认签到_{activity_id}.png")
        create_sign_qrcode(activity_id, default_sign_id, button_type=1, button_name="签到", output_file=sign_file)

        signout_file = os.path.join(activity_dir, f"默认签退_{activity_id}.png")
        create_sign_qrcode(activity_id, default_signout_id, button_type=2, button_name="签退", output_file=signout_file)

    print(f"已在目录 {activity_dir} 中生成所有二维码")


# 示例调用
if __name__ == "__main__":
    # 你可以替换成你的 activityId
    activity_id = "11550"

    # 方法1: 只生成现场报道二维码
    create_report_qrcode(activity_id, filename="activity_report_qrcode.png")
