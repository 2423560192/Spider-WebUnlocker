# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymysql


class MyspiderPipeline:
    def __init__(self):
        # 链接数据库
        self.db = pymysql.connect(
            user='root',
            password='root',
            database='learn',
            host='127.0.0.1',
            port=3306,
        )
        self.cursor = self.db.cursor()
        # 创建数据库表
        try:
            sql = 'create table 链家二手房(id int not null auto_increment primary key ,name varchar(255),price varchar(255),link varchar(255),content varchar(255),area varchar(255))'
            self.cursor.execute(sql)
        except Exception as e:
            print('表已存在!',e)

    # 该方法名为固定的 不可以更改
    def process_item(self, item, spider):
        # 保存为数据库
        dict_data = dict(item)
        lst = lst = list(map(lambda x:x,dict_data.values()))
        sql = 'insert into 链家二手房(name,price,link,content,area) values ("%s","%s","%s","%s","%s")'
        print(lst)
        self.cursor.execute(sql,lst)
        self.db.commit()

        return item

