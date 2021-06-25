# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PeipeichaItem(scrapy.Item):
    # define the fields for your item here like:
    collect_url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
