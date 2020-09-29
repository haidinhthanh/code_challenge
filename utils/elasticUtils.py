def is_index_exist_in_elastic(elastic, index):
    """
    check if index is exist in cluster elastic
    :param elastic: elastic client object
        Elastic search client object
    :param index: str
        Name of index
    :return: bool
        True if exist index else False
    """
    if elastic.indices.exists(index=index):
        return True
    return False


def create_index_in_elastic(elastic, index):
    """
    Create new index in elastic search
    :param elastic: elastic client object
        Elastic search client object
    :param index: str
        Name of index
    :return: tuple (bool, result)
        bool: result create index
        result: dict detail result create index
    """
    result = elastic.indices.create(index=index, ignore=400)
    if result and result["acknowledged"]:
        return True, result
    else:
        return False, result


def mapping_to_index_in_elastic(elastic, index):
    """
    Create mapping for index
    :param elastic: elastic client object
        Elastic search client object
    :param index: str
        Name of index
    :return: tuple (bool, result)
        bool: result mapping index
        result: dict detail result mapping index
    """
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
    """
    Set max result hits return when search in specific index
    :param elastic: elastic client object
        Elastic search client object
    :param index: str
        Name of index
    :param max_result: int
        Number of max hits
    :return: dict
        Result of setting max hits return
    """
    body = {
        "index": {
            "max_result_window": max_result
        }
    }

    result = elastic.indices.put_settings(index=index,
                                          body=body)
    return result
