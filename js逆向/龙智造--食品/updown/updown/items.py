# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 获取id
class UpdownItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    place = scrapy.Field()
    kind = scrapy.Field()
    category = scrapy.Field()

# 企业基础信息
class Baseinfo(scrapy.Item):
    now_id = scrapy.Field()   # 目前id 1
    name = scrapy.Field()   # 企业名称 1
    oid = scrapy.Field()    # 统一社会信用代码 1
    phone = scrapy.Field()  # 联系电话 1
    email = scrapy.Field()  # 电子邮箱 1
    num = scrapy.Field()   # 从业人数 1
    addr = scrapy.Field()   # 注册地址 1
    entBrief = scrapy.Field()  # 企业简介 1
    business = scrapy.Field()  # 经营范围 1
    state = scrapy.Field()   # 企业经营状态 1
    category = scrapy.Field()   # 企业分类 1
    big_category = scrapy.Field()  # 企业大类 1
    small_category = scrapy.Field()  # 企业小类 1
    area = scrapy.Field()   # 区级 1
    city = scrapy.Field()  # 市级 1
    prevence = scrapy.Field()  # 省级 1
    reg_money = scrapy.Field()   # 注册资金 1

# 融资历程
class Rongzi(scrapy.Item):
    oid = scrapy.Field()    # 统一社会信用代码
    rongzi_round = scrapy.Field() # 融资轮次
    rongzi_money = scrapy.Field() # 融资金额
    investor = scrapy.Field()   # 投资方
    date = scrapy.Field()   #发布日期

# 严重违法
class Crime(scrapy.Item):
    oid = scrapy.Field()    # 统一社会信用代码
    date_to = scrapy.Field()    # 列入日期
    reason_to = scrapy.Field()    # 列入原因
    decison_to = scrapy.Field()    # 列入机关
    dete_out = scrapy.Field()    # 移出日期
    reason_out = scrapy.Field()    # 移出原因
    decison_out = scrapy.Field()    # 移出机关


# 经营异常
class Manage(scrapy.Item):
    oid = scrapy.Field()    # 统一社会信用代码
    date_to = scrapy.Field()    # 列入日期
    reason_to = scrapy.Field()    # 列入原因
    decison_to = scrapy.Field()    # 列入机关
    dete_out = scrapy.Field()    # 移出日期
    reason_out = scrapy.Field()    # 移出原因
    decison_out = scrapy.Field()    # 移出机关

# 行政处罚
class Administration(scrapy.Item):
    oid = scrapy.Field()  # 统一社会信用代码
    num = scrapy.Field()  # 决定文书号
    kind = scrapy.Field()  # 行政处罚种类
    decison_to = scrapy.Field()  # 决定机关
    date = scrapy.Field()  # 决定日期

# 裁决文书
class Judge(scrapy.Item):
    oid = scrapy.Field()  # 统一社会信用代码
    name = scrapy.Field()  # 案件名称
    reason = scrapy.Field()  # 案件原由
    id = scrapy.Field()  # 案件身份
    date = scrapy.Field()  # 日期
    num = scrapy.Field()  # 案号

# 股东信息
class Shareholder(scrapy.Item):
    oid = scrapy.Field()  # 统一社会信用代码
    name = scrapy.Field()  # 股东
    ratio = scrapy.Field()  # 持股比例
    money = scrapy.Field()  # 认缴出资额
    date = scrapy.Field()  # 发布日期


