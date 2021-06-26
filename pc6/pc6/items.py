# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Pc6Item(scrapy.Item):
    # define the fields for your item here like:
    collect_url = scrapy.Field() # 采集地址
    name = scrapy.Field() # app名称
    theme = scrapy.Field() # app图标
    category = scrapy.Field() # 分类
    size = scrapy.Field() # app大小
    version = scrapy.Field() # 版本号
    updated_at = scrapy.Field() # 更新时间
    auther = scrapy.Field() # 作者
    language = scrapy.Field() # 语言
    download = scrapy.Field() # app下载地址
    bundle_id = scrapy.Field() # app bundle_id
    tag = scrapy.Field() # 标签
    adaptation = scrapy.Field() # 支持设备
    img_list = scrapy.Field() # 设备截图
    introduction = scrapy.Field() # 应用介绍
    introduction_img_urls = scrapy.Field() # 应用介绍 存在图片
