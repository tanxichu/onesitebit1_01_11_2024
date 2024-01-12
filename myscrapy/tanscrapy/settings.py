#项目名
BOT_NAME = 'tanscrapy'

SPIDER_MODULES = ['tanscrapy.spiders']
NEWSPIDER_MODULE = 'tanscrapy.spiders'

# 告诉别人我提爬虫，可以注解掉
# USER_AGENT = 'MyUserAgent/1.0 (your@email.com)'  # 修改为你的User-Agent

# 若配ture即遵守对方 robots.txt规则，若false则即使对方不准也强行爬
ROBOTSTXT_OBEY = False  


# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0  

# 反防爬虫的cookie跟踪。将COOKIES_ENABLED设置为False会禁用网站在您的爬虫请求中使用Cookies，这可以减少被网站用Cookies进行反爬虫的风险。通过禁用Cookies，您可以更难以被网站识别为爬虫，因为网站通常使用Cookies来跟踪用户的会话状态和行为，以识别潜在的爬虫活动。
COOKIES_ENABLED = False

# 正常是不用telnet
# TELNETCONSOLE_ENABLED = False

# Override the default request headers，默认是不用修改
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'en',
# }

# 调用中间件，会更好控制。它控制了爬虫运行过程中请求和响应的处理流程。543是优先级
# 与 DOWNLOADER_MIDDLEWARES 不同，它影响的是每个具体爬虫的行为，而不是整个项目的行为。
SPIDER_MIDDLEWARES = {
    'tanscrapy.middlewares.TanscrapySpiderMiddleware': 543,
}



# Enable or disable extensions
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines，这是一个数据清洗，整理的代理。其实用处不大。可以用SQL来处理
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'tanscrapy.pipelines.TanscrapyPipeline': 300,
# }

# 当你将 AUTOTHROTTLE_ENABLED 设置为 True 时，Scrapy 会自动启用自动节流功能，
# 这意味着 Scrapy 将尝试根据目标网站的响应时间和服务器负载等因素，动态地调整发送请求的速率和下载延迟，防被关
AUTOTHROTTLE_ENABLED = True

# AUTOTHROTTLE_START_DELAY 设置了在启动爬虫时的初始下载延迟，单位是秒。这个值表示爬虫启动
# 后第一次发送请求之前的等待时间。在启动时，自动限速会等待一段时间，然后开始发送请求，之后会根据服务器的响应时间和其他因素来动态地调整请求速率。
AUTOTHROTTLE_START_DELAY = 0.1

# The maximum download delay to be set in case of high latencies，专门针对下载的。可以注解掉
# AUTOTHROTTLE_MAX_DELAY = 60


# Configure maximum concurrent requests performed by Scrapy (default: 16)，本处是同一时间是32个
# CONCURRENT_REQUESTS：在没有启动自动调速时，最大的请求数。
CONCURRENT_REQUESTS = 32

# 每秒并发请求数量，这个是开启了自动调速后最大的请求数，与上面的是二选一的关系。AUTOTHROTTLE_ENABLED = True这个要开启才行
AUTOTHROTTLE_TARGET_CONCURRENCY = 32

# 不开启日志监测
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)。这个用缓存让采集得更快，同时对反防爬虫没关
HTTPCACHE_ENABLED = True
# 默认是0，即永远不过期。应设为正整数，如3，即3秒内同一个数据的，它可能就不再更新的了，而是以缓存给你发回来。
HTTPCACHE_EXPIRATION_SECS = 3
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Configure logging
LOG_LEVEL = 'WARNING'  # 设置日志级别为WARNING，若配为INFO的，会有更多信息
CONCURRENT_REQUESTS_PER_DOMAIN = 32  # 默认也是16，适度增加


# 此处的downloader中间件，不是特指下载音频、视频、图片的，而是针对整个网站的。就算是采集titleb 也与它有关
# 要将全部的 DOWNLOADER_MIDDLEWARES 放在一起，不能单独放，否则新的会重写旧的
DOWNLOADER_MIDDLEWARES = {
    #读取middlewares.py文件下的 RandomUserAgentMiddleware的一个方法，
    'tanscrapy.middlewares.RandomUserAgentMiddleware': 543,
    # 启动中间件的优化，注，它不是只针对下载图片的，普通的txt也有作用的
    'tanscrapy.middlewares.TanscrapyDownloaderMiddleware': 543,
}

















