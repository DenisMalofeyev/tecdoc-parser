from scrapy.spider import Spider
from scrapy.selector import Selector

from src.items import Part


class ExistSpider(Spider):
    name = 'exist_spider'
    allowed_domains = ['exist.ru']
    start_urls = ['https://www.exist.ru/cat/TecDoc']

    def parse(self, response):
        sel = Selector(response)
        marks_links = sel.xpath('//a[re:test(@href, "/cat/TecDoc/Cars/")]//@href').extract()
        for link in marks_links:
            print link