"""
爬取一本书的单词
"""
import imghdr
import os
import re

import pandas as pd
import requests
from jsonpath_ng import parse


def get_parse_data(data):
    result = {}
    for unit in data['data']:
        title = unit['title']
        words = unit['words']
        result[title] = []

        for word in words:
            en = word.get('en')
            zh = word.get('zh')
            style = word.get('style', None)  # 如果没有 style，设为 None
            result[title].append({
                'en': en,
                'zh': zh,
                'style': style
            })

    # 打印结果
    return result


def get_resp_data(id):
    headers = {
        'Host': 'api.lelegs.net',
        'xweb_xhr': '1',
        'userid': '67e1f46e4ffa83fb6914fc2d',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wx8390b4aaa8cbabff/45/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    params = {
        'book_id': id,
    }

    response = requests.get('https://api.lelegs.net/yytx-v2/book/getWords', params=params, headers=headers)
    data = response.json()
    return data


def save_data(data, name, save_path):
    # 创建输出目录
    print('保存:', data)
    output_dir = f"{save_path}/{name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 为每个单元生成 Excel 文件
    for unit, words in data.items():
        # 创建 DataFrame
        df = pd.DataFrame(words, columns=['en', 'zh', 'style'])
        # 清理文件名中的非法字符
        unit_cleaned = re.sub(r'[<>:"/\\|?*]', '_', unit)  # 替换非法字符为下划线
        # 将文件名中的空格替换为下划线，避免文件路径问题
        filename = f"{unit_cleaned}.xlsx"
        file_path = os.path.join(output_dir, filename)

        # 保存到 Excel
        df.to_excel(file_path, index=False)
        print(f"已生成: {file_path}")

    print("所有单元的 Excel 文件已生成！")


def save_img_data(name, img_url, save_path):
    """
    从图片链接下载并保存图片到指定路径。

    参数:
        name (str): 图片名称（不含扩展名）
        img_url (str): 图片的链接（URL）
        save_path (str): 保存路径的根目录
    """
    try:
        # 下载图片
        response = requests.get(img_url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        img_data = response.content  # 获取图片的二进制数据

        # 创建输出目录
        output_dir = os.path.join(save_path, name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 检测图片格式（如果可能）
        img_format = imghdr.what(None, img_data)  # 从二进制数据推断格式
        if not img_format:
            # 如果无法检测格式，尝试从 URL 中提取扩展名
            img_format = img_url.split('.')[-1].lower()  # 例如从 "image.jpg" 中提取 "jpg"
            if img_format not in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                img_format = 'jpg'  # 默认使用 jpg

        # 清理文件名中的非法字符
        name_cleaned = re.sub(r'[<>:"/\\|?*]', '_', name)
        img_filename = f"{name_cleaned}.{img_format}"
        img_path = os.path.join(output_dir, img_filename)

        # 保存图片
        with open(img_path, 'wb') as f:
            f.write(img_data)
        print(f"图片已保存: {img_path}")

    except requests.exceptions.RequestException as e:
        print(f"下载图片失败: {e}")
    except Exception as e:
        print(f"保存图片失败: {e}")


def get_data(id, name, img, save_path):
    """
    获取一本书的数据
    :return:
    """
    resp_data = get_resp_data(id)
    res = get_parse_data(resp_data)
    # # 保存数据
    save_data(res, name, save_path)
    # save_img_data(name, img, save_path)  # 保存图片
