domain_news_xpath = {
    "vnexpress.net": {
        "the thao": {
            "category": ["thể thao"],
            "published_time": [
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
            ]
        },
        "kinh doanh": {
            "category": ["kinh doanh"],
            "published_time": [
                '//div[@class="wrap-date-cat flexbox"]/span[@class="date"]/text()'
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
            ]
        }
    }
}
