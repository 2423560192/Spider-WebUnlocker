import os
import random
import time

import get_books
import get_banben
import get_source
from js逆向.口袋开言 import get_catalog, get_book_img, get_word
from js逆向.口袋开言.utils.save import get_save_img_url, save_img

if __name__ == '__main__':

    # 获取版本
    banbens = get_banben.get_data()

    # 遍历版本
    i = 0
    for banben in banbens:
        print("当前：", i, banben)
        i += 1
        # 基础路径
        base_path = '口袋开言-英语书'

        if not os.path.exists(base_path):
            os.mkdir(base_path)

        b_id = banben['id']
        b_publishing = banben['publishing']

        base_path += '/' + b_publishing

        # 创建
        if not os.path.exists(base_path):
            os.mkdir(base_path)

        # 获取书名
        book_res = get_books.get_data(b_id)
        # 遍历书本
        for book in book_res:
            id = book.get('id')
            name = book.get('name')
            cover = book.get('cover')
            print('当前书：', b_publishing, name)
            # 路径
            new_path = base_path + '/' + name
            # 创建文件目录
            if not os.path.exists(new_path):
                os.mkdir(new_path)

            path = 'https://static.smallschoolbag.com/'
            # 保存封面
            # save_img(path + cover, new_path, name)
            # 保存单词
            # get_word.get_data(new_path, id)
            # 保存图文标注
            # get_book_img.get_data(id, new_path)
            # 保存图文标注目录
            # get_catalog.get_data(id, new_path)
            # 保存英语书图片
            # get_save_img_url(new_path)
            # 保存资源
            get_source.get_data(new_path, id)
            # time.sleep(random.randint(1, 3))
            # time.sleep(3)
            # break
        # break
#
