# Scrapy settings for mySpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'myspider_lianjia'

SPIDER_MODULES = ['myspider_lianjia.spiders']
NEWSPIDER_MODULE = 'myspider_lianjia.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Connection': 'keep-alive',
    'Cookie': 'SECKEY_ABVK=iYHKAbiMK0ufnuuS1Us0TrTYY6UMeUtBkDJ1Tef05nk%3D; BMAP_SECKEY=isFY573j14XKtsgmZ0N-mTOyfiVseNpfNVVD9cpFC9my3EqwjvlHdb2T8DXTFcsWh85m53F43vxVRRax9F-azTiWBrMONeA8YLCou0U3K7EIZtkg78FIA9QOg6aDsGjcTj6hFKrnAu2Ff9VjJIB71e7vQbNsd2FDJzcXyl32x5j2bpBulGZtrYzBhvEPCp1N; lianjia_uuid=92b0ce99-2085-4b68-ad31-9290315f241c; _smt_uid=64130c3c.6b49b05; _ga=GA1.2.606032075.1679020119; _jzqx=1.1679026097.1679026097.1.jzqsr=cq%2Elianjia%2Ecom|jzqct=/ershoufang/.-; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22186ea67cfe421c-0fb990600afa26-26021151-1638720-186ea67cfe56d1%22%2C%22%24device_id%22%3A%22186ea67cfe421c-0fb990600afa26-26021151-1638720-186ea67cfe56d1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; select_city=500000; _jzqckmp=1; _gid=GA1.2.511373180.1686736354; lianjia_ssid=b655bc68-98c4-450d-8365-586af158bbe0; _qzjc=1; _jzqa=1.2500649917003321300.1678969917.1686736352.1686750070.9; _jzqc=1; _jzqy=1.1682573477.1686750070.1.jzqsr=baidu.-; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1686736354,1686750073; _qzja=1.1567285060.1679022284698.1686736352022.1686750069955.1686750073022.1686750156441.0.0.0.29.7; _qzjb=1.1686750069955.3.0.0.0; _qzjto=7.2.0; _jzqb=1.3.10.1686750070.1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1686750157; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMDg3Y2Y1NzM0NWEyMWVhOTI5NGIxZWZiZTM1NTYxM2YyZDBhNmRhNDA3MDBkYmNiYjZjNWQ3NGI3MGYxMmMwNTFiZjI0MzgzNDNhNzU0NjM1YTgyYWZlNTNkODc4OWEwNmRhZjc3OWIyNTMwYTk3NWY0OGM0ZTVjNGFlYzdkMTQ0Y2RhNTlmOTA1YTRiOWEwMDg5ZDJmMmE0MjNiZTQyNmQ4MzFkZmZjYTM5NTIyYWY3ZmRmNDliODZkMWRkMmM2YzU0NTcwZWQ0MWZmYjJkN2IxN2E3YzAzZDljNDA2ODYzOGQ5MWYzNGQ3ZGMxNzQ4OGI2NWY0NTliMzM4OGJiZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJiYTRlYWQ5MFwifSIsInIiOiJodHRwczovL2NxLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvMTA2MTE0MDgzOTEzLmh0bWwiLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; lianjia_ssid=b655bc68-98c4-450d-8365-586af158bbe0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'mySpider.middlewares.MyspiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'mySpider.middlewares.MyspiderDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'myspider_lianjia.pipelines.MyspiderPipeline': 300,
    # 'mySpider.pipelines.MyspiderPipeline1': 299,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
