import scrapy
import math
from urllib import parse
from appMiCom.items import AppmicomItem

'''
https://app.mi.com/categotyAllListApi?categoryId=15&page=0&pageSize=30&type=phone
https://app.mi.com/categotyAllListApi?categoryId=15&page=0&pageSize=30&type=pad
https://app.mi.com/details?id=com.netease.blqx.mi
'''

class AppMiSpider(scrapy.Spider):
    name = 'app-mi'
    allowed_domains = ['app.mi.com']
    start_urls = [
        # 'https://app.mi.com/',
        'https://app.mi.com/details?id=com.lql.anyrate',
    ]

    def parse(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()


        content_type = response.headers.getlist('Content-Type').pop()
        url = parse.urlparse(response.url)

        if str(content_type).find('json') == -1:

             # 分类链接
            category_links = response.css('ul.category-list a::attr(href)').getall()

            for category_link in category_links:
                category_id = category_link.split('/category/')[-1]
                if category_id.isdigit():
                    next_page = f'https://app.mi.com/categotyAllListApi?categoryId={category_id}&page=0&pageSize=30'
                    yield response.follow(next_page, callback=self.parse)

            yield from response.follow_all(css='h5 a', callback=self.parse)

            # 抓取详情页面数据
            if url.path == '/details':

                bundle_id, size, version, updated_at, app_id, auther = '', '', '', '', '', ''

                for app_info_left in response.css('div.float-left'):
                    ele = app_info_left.css('div div::text').getall()
                    if len(ele) == 2:
                        if ele[0] == '软件大小':
                            size = ele[1]
                        elif ele[0] == '版本号':
                            version = ele[1]
                        elif ele[0] == '更新时间':
                            updated_at = ele[1]
                        elif ele[0] == '包名':
                            bundle_id = ele[1]

                for app_info_right in response.css('div.float-right'):
                    ele = app_info_right.css('div div::text').getall()
                    if len(ele) == 2:
                        if ele[0] == 'appID':
                            app_id = ele[1]
                        if ele[0] == '开发者':
                            auther = ele[1]
                        if ele[0] == '隐私政策':
                            pass
                        if ele[0] == '应用权限':
                            pass

                item = AppmicomItem()

                item['name'] = extract_with_css('div.app-info div.intro-titles h3::text')
                item['size'] = size
                item['theme'] = extract_with_css('div.app-info img::attr(src)')
                item['collect_url'] = response.url
                item['download'] = url.scheme + '://' + url.hostname + extract_with_css('div.app-info div.app-info-down a.download::attr(href)')
                item['bundle_id'] = bundle_id
                item['category'] = response.css('div.app-info p.special-font::text').getall()[0]
                item['adaptation'] = response.css('div.app-info p.special-font::text').getall()[1]
                item['version'] = version
                item['updated_at'] = updated_at
                item['auther'] = auther
                item['img_list'] = response.css('div.img-view img::attr(src)').getall()
                item['introduction'] = response.css('div.app-text p.pslide').getall()

                yield item

        else:

            if url.path == '/categotyAllListApi':
                query = parse.parse_qs(url.query)
                category_id = query.get('categoryId', []).pop()
                page = query.get('page', []).pop()
                count = response.json()['count']

                # 爬列表页非首页的其他页面
                if int(page) == 0 and int(count) > 30:
                    page_count = math.ceil(count / 30)
                    page_num = 1

                    while page_count > page_num:
                        next_page = f'https://app.mi.com/categotyAllListApi?categoryId={category_id}&page={page_num}&pageSize=30'
                        yield response.follow(next_page, callback=self.parse)
                        page_num += 1

                # 爬详情页
                for item in response.json()['data']:
                    next_page = f'https://app.mi.com/details?id={item["packageName"]}'
                    yield response.follow(next_page, callback=self.parse)

