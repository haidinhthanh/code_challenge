import re
from copy import deepcopy
import hashlib
from datetime import date

date_patterns = [
    {"pattern": r'\s\d{1,2}[-/]\d{1,2}[-/]\d{4}\s', "name": "fullDate"},
    {"pattern": r'\s\d{1,2}[-/]\d{4}\s', "name": "monthYearDate"},
    {"pattern": r'\s\d{1,2}[-/]\d{1,2}\s', "name": "dayMonthDate"}
]

url_patterns = [
    {"pattern": r'https?://[^\s<>"]+|www\.[^\s<>"]+', "name": "domainUrl"}
]


def remove_extra_space(text):
    """

    :param text:
    :return:
    """
    return " ".join(str(text).strip().split())


def lower_sentence(text):
    return str(text).lower()


def add_space_to_unwanted_char(text):
    """
        Add extra space around unwanted characters in the text
    :param text:
    :return:
    """
    text = re.sub(r'\n', ' ', text)
    matches = re.findall(r'[{}@_*>()\\#%+=\[\],.":;$^]', text)
    for match in matches:
        text = text.replace(match, " " + match + " ")

    return text


def replace_text_by_index(start_index, end_index, text, new_value):
    """

    :param start_index:
    :param end_index:
    :param text:
    :param new_value:
    :return:
    """
    return text[:start_index] + new_value + text[end_index:]


def find_date_entity_by_pattern(text):
    """
        Find time in sentence
    :param text: input text
    :return:
    """
    matches = re.findall(r'[{}@_*>()\\#%+=\[\],.]', text)
    for match in matches:
        text = text.replace(match, " " + match + " ")
    clone_text = remove_extra_space(text)
    match_objects = list()
    for pattern in date_patterns:
        matches = re.findall(pattern["pattern"], " " + text + " ")
        index_objects = 0
        for match in matches:
            match_objects.append({
                "entity_type": pattern["name"],
                "value": match.strip(),
                "index": index_objects
            })
            index_objects += 1
    for obj in match_objects:
        try:
            stat_index = clone_text.index(obj["value"])
            end_index = stat_index + len(obj["value"])
            clone_text = replace_text_by_index(stat_index, end_index, clone_text,
                                               " " + obj["entity_type"] + str(obj["index"]) + " ")
        except IndexError:
            print("index not found")
    replace_text = remove_extra_space(clone_text)
    return match_objects, replace_text


def find_url_entity_by_pattern(text):
    """

    :param text:
    :return:
    """
    clone_text = remove_extra_space(text)
    match_objects = list()
    for pattern in url_patterns:
        matches = re.findall(pattern["pattern"], text)
        index_objects = 0
        for match in matches:
            match_objects.append({
                "entity_type": pattern["name"],
                "value": match.strip(),
                "index": index_objects
            })
            index_objects += 1
    for obj in match_objects:
        try:
            stat_index = clone_text.index(obj["value"])
            end_index = stat_index + len(obj["value"])
            clone_text = replace_text_by_index(stat_index, end_index, clone_text,
                                               " " + obj["entity_type"] + str(obj["index"]) + " ")
        except IndexError:
            print("index not found")
    replace_text = remove_extra_space(clone_text)
    return match_objects, replace_text


def convert_entity_in_sen_to_normal(text, match_objects):
    """

    :param match_objects:
    :param text:
    :param entity_type:
    :return:
    """
    clone_text = deepcopy(text)
    for obj in match_objects:
        try:
            find_obj = obj["entity_type"] + str(obj["index"])
            stat_index = clone_text.index(find_obj)
            end_index = stat_index + len(find_obj)
            clone_text = replace_text_by_index(stat_index, end_index, clone_text, obj["value"])
        except IndexError:
            print("index not found")
            break
    return remove_extra_space(clone_text)


def create_item_id(text):
    return hashlib.md5(str(text).encode('utf-8')).hexdigest()


def get_domain(url):
    res = re.findall(r'http[s]*?://([A-Za-z_0-9.-]+).*', url)
    if res:
        return res[0]
    else:
        return None


def gen_index_name_from_domain(domain):
    today = date.today()
    today_date = today.strftime("%Y_%m_%d")
    return domain + "_" + str(today_date)