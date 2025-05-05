import os
import time

import pandas as pd


def save_img(cover, path, name):
    import requests

    headers = {
        'Host': 'static.smallschoolbag.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'image',
        'Referer': 'https://servicewechat.com/wxbea389fff6410981/15/page-frame.html',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = {
        'ttttt': '1',
    }

    # Replace the original urlretrieve line
    response = requests.get(
        cover,
        params=params,
        headers=headers,
        verify=False
    )

    with open(f'{path}/{name}.jpg', 'wb') as f:
        f.write(response.content)
        print(f'{path}/{name}.jpg', '保存成功')


def get_save_img_url(path):
    """
    从Excel文件中读取图片URL并下载，跳过已存在的文件，去重URL。

    参数:
        path (str): 包含Excel文件和保存图片的目录路径。
    """
    # 读取指定路径下的Excel文件“图文标注.xlsx”
    try:
        df = pd.read_excel(os.path.join(path, '图文标注.xlsx'))
        # 从DataFrame中提取“image_path”列，去除空值并转换为列表，然后去重

        img_urls = list(set(df['image_path'].dropna().tolist()))  # 使用set去重后转回list
    except:
        return
    # 定义保存图片的目录
    save_dir = os.path.join(path, '英语电子书图片')
    # 如果保存目录不存在，则创建它
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 遍历所有去重后的图片URL
    for url in img_urls:
        # 构造完整的图片URL，添加域名前缀
        new_url = 'https://static.smallschoolbag.com/' + url
        # 从URL中提取文件名（取最后一部分，去掉扩展名）
        filename = url.split('/')[-1].split('.')[0]
        # 构造完整的保存路径
        save_path = os.path.join(save_dir, f"{filename}.jpg")

        # 检查文件是否已存在，若存在则跳过
        if os.path.exists(save_path):
            print(f"已跳过（文件已存在）: {save_path}")
            continue

        # 下载并保存图片
        save_img(new_url, save_dir, filename)
        # 暂停0.5秒，避免过于频繁地请求服务器
        time.sleep(0.5)
