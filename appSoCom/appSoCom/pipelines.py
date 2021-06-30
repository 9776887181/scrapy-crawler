# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter, adapter
import sys
import scrapy
import logging
import json
import os
from scrapy.utils.python import to_bytes
from urllib.parse import urlparse

sys.path.append( os.path.join(os.getcwd(), os.pardir) )

from common.mysql import Mysql
from common.redis import Redis
from common.helpers import test
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from datetime import datetime


class AppsocomPipeline:
    def process_item(self, item, spider):
        return item


class AppsocomImagesPipeline(ImagesPipeline): 

    def file_path(self, request, response=None, info=None, *, item=None):
        path = super().file_path(request, response=response, info=info, item=item)
        now = datetime.now().strftime("%Y%m%d")
        return f'{path.replace("full", now)}' 

    def get_media_requests(self, item, info):
        for image_url in item['image_list']:
            if image_url is not None:
                yield scrapy.Request(image_url)   

        for theme in item['theme']:
            if theme is not None:
                yield scrapy.Request(theme)
         

    def item_completed(self, results, item, info):
        image_list, theme = [], []

        for ok, x in results:
            if ok:
                if x['url'] in item['theme']:
                    theme.append(x['path'])
                else:
                    image_list.append(x['path'])

        adapter = ItemAdapter(item)
        adapter['theme'] = theme 
        adapter['image_list'] = image_list

        return item


class AppmicomMysqlPipeline:

    def __init__(self) -> None:
        self.dbpool = Mysql.connect()

    
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item) # 调用插入的方法
        query.addErrback(self._handle_error, item, spider) # 调用异常处理方法
        return item


    def _conditional_insert(self, tx, item):

        Redis.connect().set(item['collect_url'], f'{item["version"]}')

        create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "INSERT INTO applications_1(`name`, `collect_url`, `type`,  `theme`, `category`, `size`, `version`, `updated_at`, `auther`, `language`, `download`, `bundle_id`, `tag`, `adaptation`, `image_list`, `introduction`, `create_at`)"
        sql += " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (
            item['name'],
            item['collect_url'],
            item['type'],
            json.dumps(item['theme']),
            item['category'],
            item['size'],
            item['version'],
            item['updated_at'],
            item['auther'],
            item['language'],
            item['download'],
            item['bundle_id'],
            item['tag'],
            item['adaptation'],
            json.dumps(item['image_list']),
            item['introduction'],
            create_at
        )

        tx.execute(sql, params)


    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print('--------------database operation exception!!-----------------')
        print('-------------------------------------------------------------')
        print(failue)


