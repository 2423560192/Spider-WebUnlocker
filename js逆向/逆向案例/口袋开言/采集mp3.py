import os
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

# Excel 文件名
excel_file = 'D:\projects\Spider-WebUnlocker\js逆向\逆向案例\口袋开言\ebook_images.xlsx'
# 目标列名
column_name = 'sound_path'
# 下载目录
download_dir = 'D:\projects\Spider-WebUnlocker\js逆向\逆向案例\口袋开言\downloaded_mp3'
# URL 前缀
url_prefix = 'https://static.smallschoolbag.com/'

# 创建保存目录（如果不存在）
os.makedirs(download_dir, exist_ok=True)

# 读取 Excel 文件
df = pd.read_excel(excel_file)

# 检查列是否存在
if column_name not in df.columns:
    raise ValueError(f"列 '{column_name}' 不存在于 Excel 文件中")

# 提取所有的音频路径
paths = df[column_name].dropna().unique()

pool = ThreadPoolExecutor(10)


def download(url, full_url):
    try:
        print(f"正在下载：{url}")

        response = requests.get(url)
        response.raise_for_status()  # 检查是否请求成功

        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"保存成功：{file_path}")

    except requests.exceptions.RequestException as e:
        print(f"下载失败：{full_url} 错误信息：{e}")


# 下载所有音频文件
for path in paths:
    full_url = url_prefix + path
    file_name = os.path.basename(path)
    file_path = os.path.join(download_dir, file_name)

    if os.path.exists(file_path):
        # print(file_name, '已采集')
        continue
    # print(full_url)
    pool.submit(download, full_url, file_path)
