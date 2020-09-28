import configparser
from os import path
from newspaper_crawl.constant.path import URL_PATH
from newspaper_crawl.constant.constant import DOMAIN_AVAILABLE
from newspaper_crawl.utils.fileUtils import is_file_exist

config = configparser.RawConfigParser()
config.read(path.join(URL_PATH, 'config.properties'))


def get_url_save_dir_by_domain(domain):
    if domain in DOMAIN_AVAILABLE:
        return config.get("map_dir_url", domain)
    else:
        return None


def get_urls_from_file_by_date(domain, date_str):
    newspaper_dir = get_url_save_dir_by_domain(domain)
    file_name = str(date_str) + ".txt"
    file_full_path = path.join(URL_PATH, newspaper_dir, file_name)
    if is_file_exist(file_full_path):
        with open(file_full_path, "r+", encoding="utf8") as file:
            lines = file.readlines()
            return lines
    else:
        return []

