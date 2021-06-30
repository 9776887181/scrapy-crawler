# Scrapy settings for appSoCom project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import sys

sys.path.append( os.path.join(os.getcwd(), os.pardir) )

from common.config import Config

BOT_NAME = 'appSoCom'

SPIDER_MODULES = ['appSoCom.spiders']
NEWSPIDER_MODULE = 'appSoCom.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'appSoCom (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'appSoCom.middlewares.AppsocomSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'appSoCom.middlewares.AppsocomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
   'appSoCom.pipelines.AppsocomImagesPipeline': 300,
   'appSoCom.pipelines.AppmicomMysqlPipeline': 200,
   # 'appSoCom.pipelines.AppsocomPipeline': 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

IMAGES_STORE = f'ftp://{Config.get("ftp", "host")}:{Config.get("ftp", "prot")}'
# IMAGES_URLS_FIELD = 'image_list'

# IMAGES_STORE = 'images'

FILES_STORE = f'ftp://{Config.get("ftp", "host")}:{Config.get("ftp", "prot")}'

# FILES_STORE = 'files'


DOWNLOAD_FAIL_ON_DATALOSS = False

FEED_STORAGE_FTP_ACTIVE = True

FTP_USER = Config.get('ftp', 'user')
FTP_PASSWORD = Config.get('ftp', 'passwd')
FTP_PASSIVE_MODE = False



# 自动限制爬行速度
AUTOTHROTTLE_ENABLED = True

# 初始下载延迟（秒）
AUTOTHROTTLE_START_DELAY = 5

# 在高延迟情况下设置的最大下载延迟（秒）
AUTOTHROTTLE_MAX_DELAY = 60

# Scrapy的平均请求数应与远程网站并行发送
AUTOTHROTTLE_TARGET_CONCURRENCY = 1

# 调试模式
AUTOTHROTTLE_DEBUG = True