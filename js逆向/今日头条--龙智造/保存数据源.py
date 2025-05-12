import pandas as pd
import pymysql as pymysql

df = pd.read_excel('资讯新闻.xlsx')

# 链接数据库
db = pymysql.connect(
        user='root',
        password='root',
        database='龙智造企业数据',
        host='127.0.0.1',
        port=3306
)
cursor = db.cursor()

for k,v in df.iterrows():
    lst = list(v)
    print(lst)
    sql = 'insert into 资讯新闻(标题,对应企业,链接地址,发布日期,文章内容,关键词) values ("%s","%s","%s","%s","%s","%s")'
    cursor.execute(sql, lst)
    db.commit()
