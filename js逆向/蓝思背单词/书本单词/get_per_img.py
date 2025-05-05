"""
小程序：蓝思背单词
获取一本书下面的所有单元单词
免责声明：
本代码仅供学习和参考之用，不得用于任何商业用途或非法目的。使用者应自行承担因使用本代码所产生的一切后果和风险，包括但不限于数据丢失、系统损坏或法律责任。作者不对代码的完整性、准确性或适用性作出任何明示或暗示的保证。使用本代码前，请确保遵守相关法律法规和目标网站的使用条款。
"""
import json
import os
import random
import time
import re

import execjs
import pandas as pd
import requests
from jsonpath_ng import parse

from utils.decrypt_js import jiemi


def get_resp_data(lgid):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1 wechatdevtools/1.06.2412050 MicroMessenger/8.0.5 Language/zh_CN webview/',
        'content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx9ca23b910f46dcde/devtools/page-frame.html',
    }

    data = f'lgid={lgid}&type=learn&appCookie=version_8.0.5%20build_18%20pro_0%20lan_zh_CN%20oid_%20package_com.miniapp.lsbdc%20platform_devtools%20ver_1%20model_iPhone-12%2F13%20(Pro)%20t2_1742814109%20t_1742813790%20md5_7d%20uid_0%20di_0%20wh_390x753'

    response = requests.post('https://dudu.diiiapp.com/app/word/words', headers=headers, data=data)

    data = response.json()
    return data


def get_data(title, lgid):
    data = get_resp_data(lgid)
    # 解密
    data = jiemi(data)
    # 解析
    parse_data(title, data)



def parse_data(title, data):
    # 定义 JSONPath 表达式
    word_expr = parse('$.list[*].word')  # 用于提取数据中的单词
    imgs = parse('$.list[*].img')  # 用于提取数据中的图片路径

    # 提取数据
    words = [match.value for match in word_expr.find(data)]  # 获取所有单词列表
    imgs = [match.value for match in imgs.find(data)]  # 获取所有图片路径列表

    # 如果目录不存在，则创建目录
    os.makedirs(title, exist_ok=True)

    # 定义清理文件名的函数
    def sanitize_filename(filename):
        # 移除非法字符并替换为下划线
        invalid_chars = '<>:"/\\|?*'  # 定义文件名中不允许的特殊字符
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        # 移除连续的多个下划线
        filename = re.sub(r'_+', '_', filename)
        # 去除首尾的空白字符和下划线
        filename = filename.strip().strip('_')
        return filename

    # 处理单词和图片
    for word, img in zip(words, imgs):
        try:
            # 清理单词以生成安全的文件名
            safe_word = sanitize_filename(word.lower())  # 转换为小写并清理
            if not safe_word:  # 检查清理后文件名是否为空
                safe_word = "unnamed_" + str(time.time()).replace('.', '')  # 如果为空，使用时间戳生成唯一文件名

            # 定义文件保存路径
            file_path = os.path.join(title, f"{safe_word}.jpg")

            # 检查文件是否已存在
            if os.path.exists(file_path):
                print(f"文件已存在，跳过保存: {word} ({safe_word}.jpg)")
                continue  # 跳过当前循环，不下载和保存

            # 下载并保存图片
            url = "https://gdl.tenlearn.cn/dict/" + img  # 构造完整的图片URL
            response = requests.get(url, stream=True, timeout=10)  # 发送请求，设置10秒超时
            response.raise_for_status()  # 检查请求是否成功，若失败则抛出异常

            # 保存图片
            with open(file_path, "wb") as f:  # 以二进制写模式打开文件
                for chunk in response.iter_content(1024):  # 按块读取内容
                    f.write(chunk)  # 写入文件

            print(f"图片保存成功: {word} (保存为 {safe_word}.jpg)")  # 打印成功信息

        except requests.exceptions.RequestException as e:
            print(f"保存图片失败: {word} - {img}, 网络错误: {e}")  # 网络相关的错误
        except IOError as e:
            print(f"保存图片失败: {word} - {img}, 文件写入错误: {e}")  # 文件操作相关的错误
        except Exception as e:
            print(f"保存图片失败: {word} - {img}, 未知错误: {e}")  # 其他未知错误

        time.sleep(0.3)  # 限速，每次请求间隔0.3秒，避免请求过快
