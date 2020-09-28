import re
import hashlib
from datetime import date


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


def create_item_id(text):
    return hashlib.md5(str(text).encode('utf-8')).hexdigest()


def get_time_from_string_by_pattern(text):
    pattern = r"(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{1,2})"
    matches = re.findall(pattern, text)
    print(matches)

get_time_from_string_by_pattern(" hứ hai, 28/9/2020, 00:00 ")
