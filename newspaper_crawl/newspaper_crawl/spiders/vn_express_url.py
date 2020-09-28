import scrapy
from scrapy.loader import ItemLoader
from newspaper_crawl.constant.xpath import category_xpath
from newspaper_crawl.utils.urlUtils import get_url_save_dir_by_domain
from os import path
from newspaper_crawl.constant.path import URL_PATH
from newspaper_crawl.items import UrlItem


class VnExpressUrlSpider(scrapy.Spider):
    name = 'vn_express_url_crawler'
    allowed_domains = ['vnexpress.net']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipelines = ["NewsUrlPipeline"]
        self.domain = self.allowed_domains[0]
        self.start_urls = category_xpath[self.domain]["urls"]
        self.next_page_xpath = category_xpath[self.domain]["first_next_page"]
        self.save_dir = get_url_save_dir_by_domain(self.domain)
        self.url_save_path = path.join(URL_PATH, self.save_dir)

    def parse(self, response):
        item = UrlItem()
        urls = list()
        for xpath in self.next_page_xpath:
            page_links = response.xpath(xpath).getall()
            urls += page_links
        item["urls"] = urls
        item["save_path"] = self.url_save_path
        yield item
