import scrapy
from urllib import parse


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.peipeicha.com']
    start_urls = [
        'https://www.peipeicha.com/'
    ]

    def parse(self, response):

        url = parse.urlparse(response.url)

        links = response.css('div.ft a::attr(href), div.new-img a::attr(href), nav.new-nav a::attr(href), .pagination a::attr(href), a.head::attr(href), div.box-img a::attr(href), div.nav-title a::attr(href)').getall()

        for link in links:
            if link is not None:
                if not link.startswith('javascript'):
                    yield response.follow(link, self.parse)

        quote = response.css('div.middle-text')

        urls = quote.css('img::attr(src)').getall()

        image_urls = []
        for image_url in urls:
            image_urls.append(url.scheme + '://' + url.hostname + image_url)

        if url.path.startswith('/article'):
            yield {
                'collect_url': url.path,
                'title': response.css('h1::text').get(),
                'content': quote.get(),
                'image_urls': image_urls,
            }
