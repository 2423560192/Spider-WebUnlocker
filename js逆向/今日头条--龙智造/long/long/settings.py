# Scrapy settings for long project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "long"

SPIDER_MODULES = ["long.spiders"]
NEWSPIDER_MODULE = "long.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

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
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Connection': 'keep-alive',
  'Cookie': 'tt_webid=7258836829079619109; ttcid=56259e8c266641979d09086af90d8ea533; local_city_cache=%E9%87%8D%E5%BA%86; csrftoken=fb344a7ae558cb3f89b663acfbc1d4d6; _ga=GA1.1.1082566593.1690079680; s_v_web_id=verify_lkett0s7_M7ejhUQ7_FSBX_4jR9_9XSL_Y2M312necU10; _ga_QEHZPBE5HH=GS1.1.1690082770.2.1.1690082774.0.0.0; tt_scid=baErKrfSs4mLzRuqZ6wPH3lc.M5QK1azc2kXJdPljI-k1lwq8R90Ok3amvK4Pnff0908; ttwid=1%7Cc5R02YaeENM7O-EQCl9r1WmoamAVVt4cTDc61UhF3Q0%7C1690082761%7C6c55c4bf8df5473c6c48434db86f94d4bcbb9a5a65062e07a33bebaff361661f; msToken=HD1IHgvSnx7El6o35qOykR3MJ18uy-GFmi3rcYMHT5DOgyhBvOeCjWKjeKSAYT3b9DRL-_rbgaLRp4pwW3aUa_Umje_4GtxAR5bADY3g',
  'Referer': 'https://landing.toutiao.com/',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "long.middlewares.LongSpiderMiddleware": 543,
# }


# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "long.middlewares.LongDownloaderMiddleware": 543,
    "long.middlewares.UADownloaderMiddleware": 200,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "long.pipelines.LongPipeline": 300,
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
