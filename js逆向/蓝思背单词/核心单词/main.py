"""
获取小学每一本书的单词，并分别保存在每一本书对应的excel中
免责声明：
本代码仅供学习和参考之用，不得用于任何商业用途或非法目的。使用者应自行承担因使用本代码所产生的一切后果和风险，包括但不限于数据丢失、系统损坏或法律责任。作者不对代码的完整性、准确性或适用性作出任何明示或暗示的保证。使用本代码前，请确保遵守相关法律法规和目标网站的使用条款。
"""
import os
import random
import time

import pandas as pd

import get_unit_pid
from utils.decrypt_js import jiemi
import get_per_img

if __name__ == '__main__':
    excel_file = "book_ids.xlsx"
    # 从 Excel 中读取书本 ID，并跳过已处理的
    df = pd.read_excel(excel_file)
    ids = df["Book_ID"].tolist()  # 获取所有 ID
    processed_status = df["Processed"].tolist()  # 获取处理状态
    # 筛选未处理的 ID
    unprocessed_ids = [id_ for id_, processed in zip(ids, processed_status) if not processed]
    print("未处理的书本 ID:", unprocessed_ids)
    if not os.path.exists('书籍图片'):
        os.mkdir('书籍图片')
    # 遍历未处理的 ID 并处理
    for i in unprocessed_ids:
        # 获取一本书的所有单元
        resp_data = get_unit_pid.get_resp_data(i)

        # 解密数据
        data = jiemi(resp_data)

        # 解析单元数据
        data = get_unit_pid.get_parse_data(data)

        # 设置保存目录
        title = '书籍图片'  # 可改为 data['title'] 以使用动态书名
        units = data['unit']

        # 遍历每个单元
        for unit in units:
            print(f"当前处理的书本 ID: {i}")
            uni_title = unit['title']  # 单元标题
            lgid = unit['lgid']  # 单元 lgid

            # 爬取图片
            get_per_img.get_data(title, lgid)

            # 随机休眠 1-3 秒，避免请求过快
            time.sleep(random.randint(1, 2))
            # break

        # 跑完一个 ID 后打标签并更新 Excel
        print(f"【完成标签】书本 ID {i} 处理完成")

        # 更新 Excel 中的 Processed 列
        df.loc[df["Book_ID"] == i, "Processed"] = True
        df.to_excel(excel_file, index=False)  # 保存更新后的 Excel

        # 随机休眠 2-5 秒，避免频繁请求
        time.sleep(random.randint(1, 3))
        # break

    print("所有未处理的书本处理完成！")
