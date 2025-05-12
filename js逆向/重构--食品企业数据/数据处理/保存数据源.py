import pymysql
import pandas as pd
db = pymysql.connect(
        user='root',
        password='root',
        database='临时2',
        host='127.0.0.1',
        port=3306,
)
cursor = db.cursor()

db2 = pymysql.connect(
        user='root',
        password='root',
        database='临时',
        host='127.0.0.1',
        port=3306,
    )
cursor2 = db2.cursor()
sql = 'select * from 企业基础信息'
cursor.execute(sql)
results = cursor.fetchall()
for i in results:
    i = list(i)
    if '市' in i[14]:
        i[13] = i[14]
        i[14] = '-'
    print(i)
    try:
        sql = 'insert into 企业基础信息(统一社会信用代码,企业名称, 电话,邮箱,从业人数,地址,企业简介,经营范围,状态,分类,行业大类,行业小类,区级,市级,省级,注册金额) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
        cursor2.execute(sql, i)
        db2.commit()
    except Exception as e:
        print(e)




# df = pd.read_excel('基础信息2.xlsx')
# for k,v in df.iterrows():
#     v['统一社会信用代码'] = str(v['统一社会信用代码'])
#     info = list(v)[1:]
#     print(info)
#     try:
#         sql = 'insert into 企业基础信息(统一社会信用代码,企业名称, 电话,邮箱,从业人数,地址,企业简介,经营范围,状态,分类,行业大类,行业小类,区级,市级,省级,注册金额) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
#         cursor.execute(sql, info)
#         db.commit()
#     except Exception as e:
#         print(e)

# 写入基本信息1
# df = pd.read_excel('info1.xlsx')
# for k,v in df.iterrows():
#     info = list(v)[1:]
#     print(info)
#     try:
#         sql = 'insert into 企业基础信息1(市级, 省级,区级,状态,分类,ids, 电话,邮箱,企业名称,注册金额,企业简介,行业大类,行业小类,地址) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
#         cursor.execute(sql, info)
#         db.commit()
#     except Exception as e:
#         print(e)

# 写入经营信息
# df = pd.read_excel('经营 (1).xlsx')
# for k,v in df.iterrows():
#     info = list(v)[1:]
#     print(info)
#     try:
#         sql = 'insert into 企业经营信息(企业统一社会信用代码,列入日期,列入经营异常名录原因,列入决定机关,移出日期,移出经营异常名录原因,移出决定机关) values ("%s","%s","%s","%s","%s","%s","%s")'
#         cursor.execute(sql, info)
#         db.commit()
#     except Exception as e:
#         print(e)

# 写入融资
# df = pd.read_excel('融资.xlsx')
# for k,v in df.iterrows():
#     info = list(v)[1:]
#     print(info)
#     try:
#         sql = 'insert into 企业融资信息(企业统一社会信用代码,融资轮次,融资金额,投资方,发布日期) values ("%s","%s","%s","%s","%s")'
#         cursor.execute(sql, info)
#         db.commit()
#     except Exception as e:
#         print(e)

# 写入行政
# df = pd.read_excel('行政.xlsx')
# for k,v in df.iterrows():
#     info = list(v)[1:]
#     print(info)
#     try:
#         sql = 'insert into 企业行政信息(企业统一社会信用代码,决定文书号,行政处罚种类,决定机关,决定日期) values ("%s","%s","%s","%s","%s")'
#         cursor.execute(sql, info)
#         db.commit()
#     except Exception as e:
#         print(e)


