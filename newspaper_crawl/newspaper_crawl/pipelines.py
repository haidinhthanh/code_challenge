from os import path
from scrapy.utils.project import get_project_settings
from elasticsearch import Elasticsearch, ElasticsearchException, ConnectionError, ConnectionTimeout
from newspaper_crawl.constant.path import LOG_PATH
from newspaper_crawl.utils.stringUtils import create_item_id, get_domain, gen_index_name_from_domain
from newspaper_crawl.utils.dateUtils import get_instance_time_iso_format
from newspaper_crawl.utils.elasticUtils import *
from newspaper_crawl.utils.logUtils import LogAction
from newspaper_crawl.utils.fileUtils import is_file_exist
from datetime import date
from newspaper_crawl.constant.xpath import news_fields


class NewspaperCrawlPipeline:
    def __init__(self):
        self.settings = get_project_settings()
        self.uri = "%s:%d" % (self.settings['ELASTIC_SEARCH_SERVER'], self.settings['ELASTIC_SEARCH_PORT'])
        self.elastic = Elasticsearch(hosts=[self.settings['ELASTIC_SEARCH_SERVER']],
                                     port=self.settings['ELASTIC_SEARCH_PORT'],
                                     timeout=90)
        self.log = LogAction(__file__).init_log(path_folder_logs=path.join(LOG_PATH, "log_pipeline_news_crawl"))
        self.news_fields = news_fields

    def process_item(self, item, spider):
        if "NewsDataPipeline" in getattr(spider, 'pipelines', []):
            index_id = create_item_id(item["url"])
            item["indexed_date"] = get_instance_time_iso_format()
            if self.check_valid_news(item):
                domain = get_domain(item["url"])
                indices = gen_index_name_from_domain(domain)
                if not is_index_exist_in_elastic(self.elastic, indices):
                    mapping_to_index_in_elastic(self.elastic, indices)
                    setting_max_result_search_index(self.elastic, indices, max_result=100)
                try:
                    for try_time in range(0, 3):
                        response = self.elastic.index(index=indices, id=index_id, body=dict(item))
                        if response["_id"] == index_id:
                            self.log.info("success index crawl data from {url}".format(url=item["url"]))
                            break
                except ElasticsearchException or ConnectionTimeout or ConnectionError:
                    self.log.info("fail index crawl data from {url}".format(url=item["url"]))
            return item
        else:
            return item

    def check_valid_news(self, news_item):
        for key, values in news_item.items():
            if key in self.news_fields:
                if key not in ["source", "author"] and not values:
                    return False
        return True


class UrlPipeline:

    def __init__(self):
        pass

    def process_item(self, item, spider):
        if "NewsUrlPipeline" in getattr(spider, 'pipelines', []):
            file_name = str(date.today().strftime("%Y_%m_%d")) + ".txt"
            file_path = item["save_path"]
            urls = item["urls"]
            full_file_path = path.join(file_path, file_name)
            if is_file_exist(full_file_path):
                with open(full_file_path, "a+", encoding="utf8") as file:
                    for url in urls:
                        file.write(url + "\n")
            else:
                with open(full_file_path, "w+", encoding="utf8") as file:
                    for url in urls:
                        file.write(url + "\n")
            return item
        else:
            return item





