import scrapy
from myspider_lianjia.items import MyspiderItem
class LianjiaSpider(scrapy.Spider):
    # 爬虫名
    name = 'lianjia'
    # 域名范围
    allowed_domains = ['lianjia.com']
    # 1.修改起始url
    start_urls = ['https://cq.lianjia.com/ershoufang/']

    def parse(self, response):
        # print("响应对象：",response)
        # print('str源码：',response.text)
        # 解析的字段
        name = response.xpath('//div[@class="title"]/a/text()').extract()  # 标题
        price = response.xpath('//div[@class="totalPrice totalPrice2"]//span/text()').extract()  # 价格
        link = response.xpath('//div[@class="title"]/a/@href').extract()  # 具体链接
        houseInfo = response.xpath('//div[@class="houseInfo"]//text()').extract()  # 具体信息
        for names,prices,links,houses in zip(name,price,link,houseInfo):
            # 3.把数据打包为整体  {}
            item = MyspiderItem()
            item["name"] = names.strip()
            item["price"] = prices+'万'
            item["link"] = response.urljoin(links)
            item["content"] = houses.replace("\n",'').strip()
            # print(item)
            # print(links)
            yield scrapy.Request(url=links,callback=self.detail,meta={'item':item})
            # print(l)
            # print('================')
            # print("组建好的item数据对象",item)
            # 4.将组建好的数据对象返回给引擎
        # 进行翻页逻辑，主要是页数选择
        for i in range(2,10):
            url = self.start_urls[0]+'pg'+str(i)
            print(url)
            yield scrapy.Request(url=url,callback=self.parse)



    def detail(self,response):
        # print(1)
        # print(response.text)
        items = response.meta['item']
        # print(items)
        area = response.xpath('//div[@class="introContent showbasemore"]//div[@class="baseattribute clear"][3]//div[@class="content"]/text()').extract()
        items['area'] = area[0].replace('\n','').strip()
        yield items


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy','crawl','lianjia','--nolog'])


