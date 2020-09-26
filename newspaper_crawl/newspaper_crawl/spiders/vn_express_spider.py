import scrapy
from scrapy.loader import ItemLoader
from newspaper_crawl.items import NewspaperItem
from newspaper_crawl.constant.xpath import domain_news_xpath


class VnExpressSpider(scrapy.Spider):
    name = 'vn_express_spider'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/mcgregor-len-lich-thuong-dai-voi-pacquiao-4167759.html']

    def parse(self, response):
        item = ItemLoader(item=NewspaperItem(), response=response)
        domain_xpath = domain_news_xpath[self.allowed_domains[0]]
        category_xpath = domain_xpath["the thao"]
        url = str(response.url)

        published_time = ""
        title = ""
        headline = ""
        content = ""
        source = ""
        category = ""
        author = ""

        for xpath in category_xpath["published_time"]:
            if xpath:
                published_time = response.xpath(xpath).get()
                if published_time:
                    break
        for xpath in category_xpath["title"]:
            if xpath:
                title = response.xpath(xpath).get()
                if title:
                    break
        for xpath in category_xpath["headline"]:
            if xpath:
                headline = response.xpath(xpath).get()
                if headline:
                    break
        for xpath in category_xpath["content"]:
            if xpath:
                content = response.xpath(xpath).getall()
                if content:
                    break
        for xpath in category_xpath["source"]:
            if xpath:
                source = response.xpath(xpath).get()
                if source:
                    break
        for xpath in category_xpath["author"]:
            if xpath:
                author = response.xpath(xpath).get()
                if author:
                    break
        for xpath in category_xpath["category"]:
            if xpath:
                category = xpath

        item.add_value("url", url)
        item.add_value("published_time", published_time)
        item.add_value("title", title)
        item.add_value("headline", headline)
        item.add_value("content", "\n ".join(content))
        item.add_value("source", source)
        item.add_value("author", author)
        item.add_value("category", category)
        print("url", url)
        print("published_time", published_time)
        print("title", title)
        print("headline", headline)
        print("content", content)
        print("source", source)
        print("author", author)
        print("category", category)
        pass
