"""
Configuration settings for Luigi workflow
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
# Set BASE_DIR to the project root (three levels up from this file)
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Data paths
INPUT_DATA_PATH = DATA_DIR / "inputs"
RAW_DATA_PATH = DATA_DIR / "raw"
PROCESSED_DATA_PATH = DATA_DIR / "processed"
OUTPUT_DATA_PATH = DATA_DIR / "outputs"

# Ensure directories exist
for path in [RAW_DATA_PATH, PROCESSED_DATA_PATH, OUTPUT_DATA_PATH, LOGS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Luigi settings
LUIGI_WORKERS = int(os.getenv("LUIGI_WORKERS", 1))

# API Configuration (example)
API_KEY = os.getenv("API_KEY", "")
API_SECRET = os.getenv("API_SECRET", "")

# Database Configuration (example)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# AWS Configuration (example)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Task specific settings
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
BATCH_SIZE = 1000


##########################################################################################
#                                SCRAPY SETTINGS                                         #
##########################################################################################
"""
Configurações do Scrapy para o projeto.
Documentação completa: https://docs.scrapy.org/en/latest/topics/settings.html
"""

BOT_NAME = "luigi_scrapy"

SPIDER_MODULES = ["pipelines_planejamento.spiders"]
NEWSPIDER_MODULE = "pipelines_planejamento.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 8
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "tasks.scrapy.middlewares.CustomSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "tasks.scrapy.middlewares.CustomDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "pipelines_planejamento.pipelines.DataValidationPipeline": 100,
    "pipelines_planejamento.pipelines.ValueNormalizationPipeline": 200,
    "pipelines_planejamento.pipelines.DuplicatesPipeline": 300,
    "pipelines_planejamento.pipelines.CsvExportPipeline": 400,
    # "pipelines_planejamento.pipelines.JsonExportPipeline": 500,  # Opcional se usar FEEDS
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
# Enable showing throttle stats for every response received:
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

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# FEEDS - Configuração para export automático
# Descomente e ajuste conforme necessário
# FEEDS = {
#     "output/%(name)s_%(time)s.jsonl": {
#         "format": "jsonlines",
#         "encoding": "utf-8",
#         "store_empty": False,
#         "overwrite": True,
#     },
# }
