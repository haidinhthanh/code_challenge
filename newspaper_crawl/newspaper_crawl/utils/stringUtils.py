import re


def get_domain(url):
    res = re.findall(r'http[s]*?://([A-Za-z_0-9.-]+).*', url)
    if res:
        return res[0]
    else:
        return None
