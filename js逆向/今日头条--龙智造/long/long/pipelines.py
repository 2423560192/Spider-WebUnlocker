# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LongPipeline:
    def __init__(self):
        # 链接数据库
        self.db = pymysql.connect(
            user='root',
            password='root',
            database='龙智造企业数据',
            host='127.0.0.1',
            port=3306
        )
        self.cursor = self.db.cursor()
        # 创建表格
        try:
            sql = 'create table 资讯新闻(id int not null auto_increment primary key,标题 varchar(255),对应企业 varchar(255),链接地址 text,发布日期 varchar(255),文章内容 TEXT,关键词 varchar(255))'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):

        lst = [item['title'],item['company'],item['link']
            ,item['date'],item['article'],item['key']]
        try:
            sql = 'insert into 资讯新闻(标题,对应企业,链接地址,发布日期,文章内容,关键词) values ("%s","%s","%s","%s","%s","%s")'
            self.cursor.execute(sql, lst)
            self.db.commit()
        except Exception as e:
            print(e)

