import scrapy
from urllib import parse
from wandoujia.items import WandoujiaItem


class AppsSpider(scrapy.Spider):
    name = 'apps'
    allowed_domains = ['www.wandoujia.com']
    start_urls = [
        # 'https://www.wandoujia.com/',
        'https://www.wandoujia.com/apps/6774394',
    ]

    def start_requests(self):
        proxy = "http://180.104.250.137:19110"
        yield scrapy.Request(self.start_urls[0], meta={"proxy": proxy})


    def parse(self, response):

        url = parse.urlparse(response.url)

        if url.path.startswith('/apps/'):

            response.text

            quote = response.css('dl.infos-list')
            print(quote)
            
            item = WandoujiaItem() 

            item['collect_url'] = response.url
            item['theme'] = response.css('div.app-icon img::attr(src)').get()
            item['name'] = response.css('div.app-info span.title::text').get()
            item['size'] = quote.xpath('/meta[@fileSize=$val]', val = 'fileSize').get()

            yield item
