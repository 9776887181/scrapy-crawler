import scrapy
import sys
import time
import json
from scrapy.item import Item
import w3lib
from urllib import parse


sys.path.append('/Users/aq/data/python-code/scrapy-crawler')

from common.helpers import url_params
from appSoCom.items import AppsocomItem


class AppsSpider(scrapy.Spider):
    name = 'apps'
    allowed_domains = ['app.so.com']
    start_urls = [
        # 'https://app.so.com/',
        # 'https://app.so.com/index/getData?page=1&type=1',
        # 'https://app.so.com/index/getData?page=1&type=2',

        #  下面分析使用URL
        'https://app.so.com/category/cat_request?page=2&requestType=ajax&_t=1624771253662&cid=3&csid=11',
        # 'https://app.so.com/detail/index?pname=Android_com.freewifi.wifishenqi&id=2528888',
    ]

    def parse(self, response):

        content_type = response.headers.getlist('Content-Type').pop()
    
        url = parse.urlparse(response.url)
        _t = str(time.time_ns())

        if str(content_type).find('json') == -1:
            for link in response.css('ul li::attr(data-href)').getall(): 
                if link is not None and link.startswith('/category/app_list'): 
                    params = url_params(link)

                    next_page = f'/category/cat_request?page=1&requestType=ajax&_t={_t[0:13]}&cid={params.get("cid")}&csid={params.get("csid")}'
                    yield response.follow(next_page, callback=self.parse)

            yield from response.follow_all(css='nav.subnav a::attr(href)', callback=self.parse)
        else:
            pass
        
        params = url_params(response.url)    

        if url.path.startswith('/category/cat_request'):
            data = json.loads(response.text)
            if len(data) > 0:
                page = int(params.get('page')) + 1
                next_page = f'/category/cat_request?page={page}&requestType=ajax&_t={_t[0:13]}&cid={params.get("cid")}&csid={params.get("csid")}'
                yield response.follow(next_page, callback=self.parse)    
                
            for item in data:
                next_page = f'/detail/index?pname={item.get("apkid")}&id={item.get("id")}'                
                yield response.follow(next_page, meta={'appinfo': item}, callback=self.detail_parse)

        elif url.path.startswith('/index/getData'):
            data = json.loads(response.text)

            if len(data.get('list')) > 0:
                page = int(params.get('page')) + 1
                next_page = f'/index/getData?page={page}&type={params.get("type")}'
                yield response.follow(next_page, callback=self.parse)   
                
            for item in data.get('list'):
                next_page = f'/category/cat_request?page=1&requestType=ajax&_t={_t[0:13]}&cid={item.get("cid")}&csid={item.get("cid2")}'
                yield response.follow(next_page, callback=self.parse)
         
   

    def detail_parse(self, response):
        appinfo = response.meta['appinfo']

        item = AppsocomItem()

        quote = response.css('div#infoMore')

        for node in quote.css('div::text').getall():
            if node is not None and node.startswith('开发者：'):
                item['auther'] = node.replace('开发者：', '') 

        for node in quote.css('div.app-moreinfo-v p::text').getall():
            if node is not None and node.startswith('更新时间：'):
                item['updated_at'] = node.replace('更新时间：', '')
            elif node is not None and node.startswith('语言：'):
                item['language'] = node.replace('语言：', '')

        item['collect_url'] = response.url
        item['type'] = appinfo.get('type')
        item['name'] = appinfo.get('name')
        item['size'] = appinfo.get('size_fixed')
        item['theme'] = [appinfo.get('logo_url')]
        item['download'] = appinfo.get('down_url')
        item['bundle_id'] = appinfo.get('apkid')
        item['category'] = appinfo.get('category_name')
        item['tag'] = appinfo.get('category_name')
        item['adaptation'] = 'android'
        item['version'] = appinfo.get('version_name')
        item['image_list'] = response.css('div.app-image img::attr(src)').getall()
        item['introduction'] = w3lib.html.remove_tags(response.css('div.app-about-full ').get(), keep=('p', 'br'))

        yield item


        
        

        


        

