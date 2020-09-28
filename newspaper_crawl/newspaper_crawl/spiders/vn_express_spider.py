import scrapy
from scrapy.loader import ItemLoader
from newspaper_crawl.items import NewspaperItem
from newspaper_crawl.constant.xpath import domain_news_xpath, news_fields
from newspaper_crawl.utils.urlUtils import get_urls_from_file_by_date
from datetime import datetime, date
import re


class VnExpressSpider(scrapy.Spider):
    name = 'vn_express_spider'
    allowed_domains = ['vnexpress.net']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = get_urls_from_file_by_date(self.allowed_domains[0], str(date.today().strftime("%Y_%m_%d")))
        self.pipelines = ["NewsDataPipeline"]

    def parse(self, response):
        item = ItemLoader(item=NewspaperItem(), response=response)
        category_xpath = domain_news_xpath[self.allowed_domains[0]]
        url = str(response.url)

        for field in news_fields:
            value = ""
            if field not in ["url", "published_time"]:
                for xpath in category_xpath[field]:
                    if xpath and field in ["content"]:
                        value = "\n ".join(response.xpath(xpath).getall())
                    elif xpath:
                        value = response.xpath(xpath).get()
                    if value:
                        break
            elif field == "url":
                value = url
            elif field == "published_time":
                for xpath in category_xpath["published_time_display"]:
                    value = response.xpath(xpath).get()
                    if value:
                        break
                time_patterns = category_xpath["time_pattern"]
                for pattern in time_patterns:
                    matches = re.findall(pattern["pattern"], value)
                    if matches:
                        news_date = matches[0][pattern["date"]]
                        news_time = matches[0][pattern["time"]] + ":00"
                        datetime_object = datetime.strptime(news_date + " " + news_time, '%d/%m/%Y %H:%M:%S')
                        value = datetime_object.isoformat()
                        break
            item.add_value(field, value)

        yield item.load_item()
