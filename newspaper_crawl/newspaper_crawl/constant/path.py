from os import path
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[2]
CRAWL_PATH = path.join(ROOT_PATH, "newspaper_crawl")
CONSTANT_PATH = path.join(CRAWL_PATH, "constant")
SPIDER_PATH = path.join(CRAWL_PATH, "spiders")
UTILS_PATH = path.join(CRAWL_PATH, "utils")
LOG_PATH = path.join(CRAWL_PATH, "log")
URL_PATH = path.join(CRAWL_PATH, "url")