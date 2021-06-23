# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AppmicomItem(scrapy.Item):
    # define the fields for your item here like:
    collect_url = scrapy.Field()
    name = scrapy.Field()
    size = scrapy.Field()
    theme = scrapy.Field()
    download = scrapy.Field()

