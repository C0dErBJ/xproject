# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Switch(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    content1 = scrapy.Field()
    sql=scrapy.Field()
