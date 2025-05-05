import os
import random
import time

import get_per_book
import get_book_words

if __name__ == '__main__':

    if not os.path.exists('英语书'):
        os.mkdir('英语书')
    grades = [
        "一年级",
        "二年级",
        "三年级",
        "四年级",
        "五年级",
        "六年级",
        "七年级",
        "八年级",
        "九年级"
    ]
    # 年级
    for grade in grades[6:]:
        # 保存数据
        save_path = f"英语书/{grade}"
        # 获取每一本书
        books = get_per_book.get_data(grade)

        # 遍历每一本书
        for book in books:
            id = book.get('_id')
            name = book.get('name')
            img = book.get('img')
            # 创建文件夹
            get_book_words.get_data(id, name, img, save_path)
            # time.sleep(random.randint(3, 6))
            time.sleep(random.randint(1, 2))
        # time.sleep(random.randint(5, 10))
        time.sleep(random.randint(1, 2))
