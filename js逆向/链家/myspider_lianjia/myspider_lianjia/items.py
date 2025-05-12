# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 标题
    price = scrapy.Field()  # 价格
    link = scrapy.Field()  # 链接
    content = scrapy.Field()  # 详情
    area = scrapy.Field() # 特色

