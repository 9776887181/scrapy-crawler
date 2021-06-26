import scrapy
from urllib import parse
from pc6.items import Pc6Item

class AppsSpider(scrapy.Spider):
    name = 'apps'
    allowed_domains = ['www.pc6.com']
    start_urls = [
        # 'http://www.pc6.com/',
        # 'http://www.pc6.com/awangyou/469_1.html',
        'http://www.pc6.com/azyx/150283.html',
        'http://www.pc6.com/azyx/105227.html',
    ]

    def parse(self, response):

        url = parse.urlparse(response.url)

        item = Pc6Item()

        if url.path.startswith('/azyx/'):

            qoute = response.css('dd#dinfo')
            nav = response.css('dt#fast-nav')

            for i in qoute.css('p.base i'):
                base_name = i.css('::text').get(default = '')
                # print(base_name)
                if base_name.startswith('类型：'):
                    pass
                elif base_name.startswith('版本：'):
                    item['version'] = base_name.replace('版本：', '')
                elif base_name.startswith('大小：'):
                    item['size'] = base_name.replace('大小：', '')
                elif base_name.startswith('更新：'):
                    item['updated_at'] = base_name.replace('更新：', '')
                elif base_name.startswith('语言：'):
                    item['language'] = base_name.replace('语言：', '')
                elif base_name.startswith('作者：'):
                    item['auther'] = i.css('s::text').get(default = '')

            sid = qoute.css('dd::attr(sid)').get(default = '')
            content = response.css('#soft-info div.intro-txt')
            category = nav.css('a::text').getall()

            if '首页' in category:
                category.remove('首页')

            if category[0].startswith('安卓'):
                adaptation = 'android'       

            # https://download.pc6.com/down/285132/  下载地址
            item['download'] = 'https://download.pc6.com/down/' + sid
                 
            item['collect_url'] = response.url
            item['name'] = qoute.css('h1::text').get(default = '')
            item['theme'] = qoute.css('p#dico img::attr(src)').get(default = '')
            item['category'] = category
            item['tag'] = qoute.css('dl.xgtag a::text').getall()
            item['introduction'] = content.get(default = '')
            item['introduction_img_urls'] = content.css('img::attr(src)').getall()
            item['img_list'] = response.css('dd#picShow li img::attr(src)').getall()
            item['adaptation'] = adaptation

            yield item        

