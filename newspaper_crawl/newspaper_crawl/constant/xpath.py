domain_news_xpath = {
    "vnexpress.net": {
        "category": ['//div[@class="header-content width_common"]/ul[@class="breadcrumb"]/li/a/text()'],
        "published_time_display": [
            '//div[@class="wrap-date-cat flexbox"]/span[@class="date"]/text()',
            '//div[@class="header-content width_common"]/span[@class="date"]/text()'],
        "title": [
            '//div[@class="section-inner inset-column special-column"]/h1/text()',
            '//div[@class="sidebar-1"]/h1[@class="title-detail"]/text()'],
        "headline": [
            '//div[@class="section-inner inset-column special-column"]/h2/text()',
            '//div[@class="sidebar-1"]/p[@class="description"]/text()'],
        "content": [
            '//div[@class="section-inner inset-column"]/p[not(@style)]/descendant-or-self::*/text()',
            '//article[@class="fck_detail "]/p[(@class="Normal") and not(@style)]/descendant-or-self::*/text()'
        ],
        "source": [None],
        "author": [
            '//div[@class="section-inner inset-column"]/p[@style="text-align:right;"]/b/text()',
            '//article[@class="fck_detail "]/p[(@class="Normal") and (@style="text-align:right;")]/strong/text()'
        ],
        "time_pattern": [
            {"pattern": r'(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{1,2})', "date": 0, "time": 1}
        ]
    }
}

category_xpath = {
    "vnexpress.net": {
        "urls": [
            "https://vnexpress.net/the-thao",
            "https://vnexpress.net/kinh-doanh",
            "https://vnexpress.net/giai-tri",
            "https://vnexpress.net/giao-duc",
            "https://vnexpress.net/phap-luat"
        ],
        "first_next_page": [
            '//article[@class="item-news full-thumb article-topstory"]/h3[@class="title-news"]/a/@href',
            '//ul[@class="list-sub-feature"]/li/h3[@class="title_news"]/a/@href',
            '//article[@class="item-news item-news-common"]/h3[@class="title-news"]/a/@href',
            '//article[@class="item-news item-news-common"]/h3[@class="title-news"]/a/@href'
        ]
    }
}
news_fields = [
    "category",
    "published_time",
    "title",
    "headline",
    "content",
    "source",
    "author",
    "url",
    "published_time_display"
]
