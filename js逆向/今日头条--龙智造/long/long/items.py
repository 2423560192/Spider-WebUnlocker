# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    company = scrapy.Field()
    key = scrapy.Field()
