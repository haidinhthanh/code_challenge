def is_index_exist_in_elastic(elastic, index):
    if elastic.indices.exists(index=index):
        return True
    return False


def create_index_in_elastic(elastic, index):
    result = elastic.indices.create(index=index, ignore=400)
    if result and result["acknowledged"]:
        return True
    else:
        return False


def mapping_to_index_in_elastic(elastic, index):
    mapping = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "text_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "char_filter": [
                            "html_strip"
                        ],
                        "filter": [
                            "lowercase",
                            "asciifolding"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "url": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text",
                    "analyzer": "text_analyzer",
                    "search_analyzer": "text_analyzer"
                },
                "headline": {
                    "type": "text",
                    "analyzer": "text_analyzer",
                    "search_analyzer": "text_analyzer"
                },
                "content": {
                    "type": "text",
                    "analyzer": "text_analyzer",
                    "search_analyzer": "text_analyzer"
                },
                "category": {
                    "type": "text",
                    "analyzer": "text_analyzer",
                    "search_analyzer": "text_analyzer"
                },
                "source": {
                    "type": "keyword"
                },
                "author": {
                    "type": "keyword"
                },
                "published_time": {
                    "type": "date"
                },
                "published_time_display":{
                    "type": "text",
                    "analyzer": "text_analyzer",
                    "search_analyzer": "text_analyzer"
                },
                "indexed_date": {
                    "type": "date"
                }
            }
        }
    }

    response = elastic.indices.create(
        index=index,
        body=mapping,
        ignore=400
    )
    if 'acknowledged' in response:
        if response['acknowledged']:
            return True, response
    elif 'error' in response:
        return False, response


def setting_max_result_search_index(elastic, index, max_result):
    body = {
        "index": {
            "max_result_window": max_result
        }
    }
    elastic.indices.put_settings(index=index,
                                 body=body)


# from elasticsearch import Elasticsearch
#
# elastic = Elasticsearch(hosts=["127.0.0.1"],
#                         port="9200",
#                         timeout=90)
# if not is_index_exist_in_elastic(elastic, "vnexpress"):
#     # create_index_in_elastic(elastic, "vnexpress")
#     mapping_to_index_in_elastic(elastic,  "vnexpress")
#     # mapping_to_index_in_elastic(self.elastic, indices)
#     # setting_max_result_search_index(self.elastic, indices, max_result=100)
#     #