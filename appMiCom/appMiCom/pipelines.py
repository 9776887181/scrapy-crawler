# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline

class AppmicomPipeline:
    def process_item(self, item, spider):
        return item


class AppmicomImagesPipeline(ImagesPipeline):

    def file_path(self, request, response, info, *, item):
        return super().file_path(request, response=response, info=info, item=item)

    def get_media_requests(self, item, info):
        return super().get_media_requests(item, info)

    def item_completed(self, results, item, info):
        return super().item_completed(results, item, info)


class AppmicomFilesPipeline(FilesPipeline):

    def file_path(self, request, response, info, *, item):
        return super().file_path(request, response=response, info=info, item=item)

    def get_media_requests(self, item, info):
        return super().get_media_requests(item, info)

    def item_completed(self, results, item, info):
        return super().item_completed(results, item, info)


class AppmicomMysqlPipeline:

    def __init__(self, dbpool) -> None:
        self.dbpool = dbpool 

    @classmethod
    def from_crawler(cls, crawler):
        dbparams = dict(
            host = crawler.settings.get('MYSQL_HOST'), # 读取settings中的配置
            db = crawler.settings.get('MYSQL_DBNAME'),
            user= crawler.settings.get('MYSQL_USER'),
            passwd = crawler.settings.get('MYSQL_PASSWD'),
            charset = 'utf8', # 编码要加上，否则可能出现中文乱码问题
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = False,    
        )

        dbpool = adbapi.ConnectionPool('pymysql', **dbparams) # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool) # 相当于dbpool付给了这个类，self中可以得到

    
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item) # 调用插入的方法
        query.addErrback(self._handle_error, item, spider) # 调用异常处理方法
        return item


    def _conditional_insert(self, tx, item):
        sql = "INSERT INTO test(`name`) VALUES(%s)"
        params = (item["name"])
        tx.execute(sql, params)


    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print('--------------database operation exception!!-----------------')
        print('-------------------------------------------------------------')
        print(failue)

