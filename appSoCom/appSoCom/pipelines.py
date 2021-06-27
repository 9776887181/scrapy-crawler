# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sys

sys.path.append('/Users/aq/data/python-code/scrapy-crawler')

from common.mysql import Mysql
from common.redis import Redis
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline


class AppsocomPipeline:
    def process_item(self, item, spider):
        return item


class AppsocomImagesPipeline(ImagesPipeline):

    # 图片保存位置
    def file_path(self, request, response, info, *, item):
        print(1)
        return super().file_path(request, response=response, info=info, item=item)

    # 图片下载请求
    def get_media_requests(self, item, info):
        print(2)
        return super().get_media_requests(item, info)

    # 
    def item_completed(self, results, item, info):
        print(3)
        return super().item_completed(results, item, info) 


