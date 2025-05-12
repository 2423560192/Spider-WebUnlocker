# Scrapy settings for updown project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "updown"

SPIDER_MODULES = ["updown.spiders"]
NEWSPIDER_MODULE = "updown.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "updown (+http://www.yourdomain.com)"

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
# 线程池
# REACTOR_THREADPOOL_MAXSIZE = 64
# 下载超时
DOWNLOAD_TIMEOUT = 0.5
# 禁止cookie
# COOKIES_ENABLED = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 300
#
# CONCURRENT_REQUESTS_PER_IP = 300

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'authority': 'holmes.taobao.com',
    'accept': 'application/json, text/plain',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'cookie': 'cna=hFmlHOLVInoCAX1SeRZobwyo; lgc=tb256721506; tracknick=tb256721506; t=05bd17d0eb125168fa7cd87059cbdca7; sgcookie=E1007p2fECijRNxbp9O1DDOfsVHbal%2Fub49b3ZDuVHI3DQ61%2FoIwVYXeerXVqhMNNPvdhctN6yFttJrZLJpae9NpkrMhbO%2FTw3gna3a9zIaL3GE%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUphzOV5nsYb%2Bf81eg%3D%3D&vt3=F8dCsf5%2BvGtOJIa4DWc%3D&nk2=F5RHpC2cIoejhjw%3D; uc4=nk4=0%40FY4MthPoY97ivHUhM%2Bj5AzTZCUJOEg%3D%3D&id4=0%40U2grF862PT9uTiwTjVJofx70LDnGzgKh; _cc_=UIHiLt3xSw%3D%3D; isg=BPX1oyCn_Rdxkxl_qTQ1aVKzBHGvcqmEDfqucXca6my7ThRAP8LlVNaHmBL4DsE8; XSRF-TOKEN=f96fdcd9-f64f-4909-b25d-20dcc5f8eb3f',
    'origin': 'https://www.dingtalk.com',
    'referer': 'https://www.dingtalk.com/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "updown.middlewares.UpdownSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "updown.middlewares.UpdownDownloaderMiddleware": 543,
    "updown.middlewares.UADownloaderMiddleware": 200,
    # "updown.middlewares.IPDownloaderMiddleware": 102,
    'updown.middlewares.ProxyDownloaderMiddleware': 102,
}
ROTATE_PROXY_INTERVAL = 20
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "updown.pipelines.UpdownPipeline": 300,
    "updown.pipelines.RongziInfo": 303,
    "updown.pipelines.CrimeInfo": 304,
    "updown.pipelines.ManageInfo": 305,
    "updown.pipelines.AdministrationInfo": 306,
    "updown.pipelines.JudgeInfo": 307,
    "updown.pipelines.ShareholderInfo": 308,
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
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
