import sys
import os
import configparser
from flask import Flask, jsonify, request
import re
import dateutil.parser
import time
from elasticsearch import Elasticsearch, ElasticsearchException, ConnectionError, ConnectionTimeout, NotFoundError
sys.path.append(os.path.dirname('../'))
from utils.logUtils import LogAction
from constant.constant import indices_pattern, news_fields
from utils.stringUtils import remove_extra_space, create_item_id, get_domain, gen_index_name_from_domain
from utils.dateUtils import get_instance_time_iso_format
from utils.elasticUtils import *

config = configparser.RawConfigParser()
config.read('config.properties')
log = LogAction(__file__).init_log(path_folder_logs=config.get("Logger", "log_path"))

app = Flask(__name__)


@app.route('/news/search', methods=['GET'])
def search_news():
    start_time = time.time()
    query = request.args.get('q')
    limit = request.args.get('limit')
    start = request.args.get('start')
    sort = request.args.get('sort')

    news_items = list()
    des = ""
    flag_valid_query = True
    query = remove_extra_space(str(query).lower())
    sort = remove_extra_space(str(sort).lower())

    if not query:
        flag_valid_query = False
        des += "query must not empty; "

    if not str(limit).isnumeric() or int(limit) <= 0:
        flag_valid_query = False
        des += "limit must be integer and bigger than 0; "

    if not str(start).isnumeric() or int(start) < 0:
        flag_valid_query = False
        des += "start must be integer and bigger or equal 0; "

    matches = re.match('^[a-z_.]*[:](asc|desc)$', sort)
    if not matches:
        flag_valid_query = False
        des += 'sort must be in form "[field]:[asc|desc]"; '

    if flag_valid_query and query and limit and start and sort:
        elastic = Elasticsearch(hosts=[config.get("Elasticsearch", "ELASTIC_SEARCH_SERVER")],
                                port=config.get("Elasticsearch", "ELASTIC_SEARCH_PORT"),
                                timeout=180)
        indices = list()
        for pattern in indices_pattern:
            indices += [idc for idc in elastic.indices.get(pattern)]
        body = dict()
        if query:
            body["query"] = {
                "query_string": {
                    "query": str(query)
                }
            }
        if limit:
            body["size"] = limit
        if start:
            body["from"] = start
        for idc in indices:
            res = elastic.search(index=idc,
                                 body=body)
            if res["hits"]["hits"]:
                news_items += res["hits"]["hits"]
        if sort:
            sort_field, type_sort = tuple(str(sort).split(":"))
            if type_sort == "asc":
                news_items.sort(key=lambda item: dateutil.parser.parse(item["_source"][sort_field]))
            elif type_sort == "desc":
                news_items.sort(key=lambda item: dateutil.parser.parse(item["_source"][sort_field]), reverse=True)
    else:
        log.info("Duration search news with param q={q}, limit={limit}, start={start}, sort={sort} is {duration}".format(
            q=query, limit=limit, start=start, sort=sort, duration=float(time.time() - start_time)
        ))
        return jsonify({
            "errorCode": 1,
            "description": des,
            "news": []
        })
    log.info("Duration search news with param q={q}, limit={limit}, start={start}, sort={sort} is {duration}".format(
        q=query, limit=limit, start=start, sort=sort, duration=float(time.time() - start_time)
    ))
    return jsonify({
        "errorCode": 0,
        "description": "success",
        "news": news_items
    })


@app.route('/news/<news_id>', methods=['PUT'])
def update_news_by_id(news_id):
    start_time = time.time()
    body = dict(request.json)
    flag_valid_params = True
    des = ""

    if not body:
        flag_valid_params = False
        des += "param must not empty; "
    if not body or not body.keys() or not set(body.keys()).issubset(set(news_fields)):
        flag_valid_params = False
        des += "param newspaper update not exist; "

    if flag_valid_params:
        elastic = Elasticsearch(hosts=[config.get("Elasticsearch", "ELASTIC_SEARCH_SERVER")],
                                port=config.get("Elasticsearch", "ELASTIC_SEARCH_PORT"),
                                timeout=180)
        indices = list()
        for pattern in indices_pattern:
            indices += [idc for idc in elastic.indices.get(pattern)]

        update_body = dict()
        update_body["script"] = dict()
        update_body["script"]["lang"] = "painless"
        inlines = list()
        for key, value in body.items():
            line = "ctx._source.{key} = '{value}';".format(key=key, value=value)
            inlines.append(line)
        inline_scripts = " ".join(inlines)
        update_body["script"]["inline"] = inline_scripts

        res = dict()
        for idc in indices:
            res = elastic.update(index=idc,
                                 id=news_id,
                                 body=update_body)
            if res and res["result"] == "updated":
                break
            elif res and "error" in res.keys():
                continue

        if res and "error" in res.keys():
            log.info("Duration update new with id = {news_id} is {duration}".format(
                news_id=news_id, duration=float(time.time() - start_time)
            ))
            return jsonify({
                "errorCode": 1,
                "description": "id not exist",
                "result": res
            })
    else:
        log.info("Duration update new with id = {news_id} is {duration}".format(
            news_id=news_id, duration=float(time.time() - start_time)
        ))
        return jsonify({
            "errorCode": 1,
            "description": des,
            "result": {}
        })
    log.info("Duration update new with id = {news_id} is {duration}".format(
        news_id=news_id, duration=float(time.time() - start_time)
    ))
    return jsonify(
        {
            "errorCode": 0,
            "description": "success",
            "result": res
        }
    )


@app.route('/news', methods=['POST'])
def add_news_item():
    start_time = time.time()
    body = dict(request.json)
    flag_valid_params = True
    des = ""
    flag_index_result = False
    item = dict()

    if not body:
        flag_valid_params = False
        des += "param must not empty; "

    if not body or not body.keys() or not set(body.keys()) == (set(news_fields)):
        flag_valid_params = False
        des += "param create newspaper item not valid or not enough field; "

    if "published_time" in body.keys():
        matches = re.match(
            r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):'
            r'([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$',
            body["published_time"])
        if not matches:
            flag_valid_params = False
            des += "param published_time is not in date iso format; "
    if "url" in body.keys():
        matches = re.match(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s("
                           r")<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,"
                           r"<>?«»“”‘’]))",
                           body["url"])
        if not matches:
            flag_valid_params = False
            des += "param url is not url format; "
    if flag_valid_params:
        response = dict()
        for key, value in body.items():
            item[key] = value
        item_id = create_item_id(item["url"])
        item["indexed_date"] = get_instance_time_iso_format()
        domain = get_domain(item["url"])
        indices = gen_index_name_from_domain(domain)

        elastic = Elasticsearch(hosts=[config.get("Elasticsearch", "ELASTIC_SEARCH_SERVER")],
                                port=config.get("Elasticsearch", "ELASTIC_SEARCH_PORT"),
                                timeout=180)
        if not is_index_exist_in_elastic(elastic, indices):
            mapping_to_index_in_elastic(elastic, indices)
            setting_max_result_search_index(elastic, indices, max_result=100)
        try:
            for try_time in range(0, 3):
                response = elastic.index(index=indices, id=item_id, body=dict(item))
                if response["_id"] == item_id:
                    log.info("success index news data from {url}".format(url=item["url"]))
                    flag_index_result = True
                    break
        except ElasticsearchException or ConnectionTimeout or ConnectionError:
            log.info("fail index news data from {url}".format(url=item["url"]))

    else:
        log.info("Duration create news fail is {duration}".format(
            duration=float(time.time() - start_time)
        ))
        return jsonify({
            "errorCode": 1,
            "description": des,
            "result": {}
        })

    if flag_index_result:
        log.info("Duration create news with id={id} is {duration}".format(
            id=item_id, duration=float(time.time() - start_time)
        ))
        return jsonify({
            "errorCode": 0,
            "description": "success",
            "result": response
        })
    else:
        log.info("Duration create news fail is {duration}".format(
            duration=float(time.time() - start_time)
        ))
        return jsonify({
            "errorCode": 1,
            "description": "fail",
            "result": response
        })


@app.route('/news/<news_id>', methods=['DELETE'])
def delete_news_by_id(news_id):
    start_time = time.time()
    elastic = Elasticsearch(hosts=[config.get("Elasticsearch", "ELASTIC_SEARCH_SERVER")],
                            port=config.get("Elasticsearch", "ELASTIC_SEARCH_PORT"),
                            timeout=180)
    indices = list()
    for pattern in indices_pattern:
        indices += [idc for idc in elastic.indices.get(pattern)]

    response = dict()
    for idc in indices:
        try:
            response = elastic.delete(index=idc, id=news_id)
        except NotFoundError:
            pass
        if response and response["result"] == "deleted":
            break
    if not (response and response["result"] == "deleted"):
        log.info("Duration delete news fail with {id} is {duration}".format(
            id=news_id ,duration=float(time.time() - start_time)
        ))
        return jsonify({
            "errorCode": 1,
            "description": "not found news id",
            "result": response
        })
    log.info("Duration delete news with {id} is {duration}".format(
        id=news_id, duration=float(time.time() - start_time)
    ))
    return jsonify({
        "errorCode": 0,
        "description": "success",
        "result": response
    })


if __name__ == '__main__':
    server_host = config.get('ServerAppSection', 'defaul.server.host')
    server_port = config.get('ServerAppSection', 'defaul.server.port')
    app.run(host=server_host, port=server_port)
