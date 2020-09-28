import scrapy
from itemloaders.processors import MapCompose, Join


def strip_space(value):
    return value.strip()


class NewspaperItem(scrapy.Item):
    url = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    published_time = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    content = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    source = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    author = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    category = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    headline = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join()
    )
    indexed_date = scrapy.Field()
    published_time_display = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join()
    )


class UrlItem(scrapy.Item):
    urls = scrapy.Field()
    save_path = scrapy.Field()
