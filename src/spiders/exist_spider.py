import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request

from src.items import Part


class ExistSpider(CrawlSpider):
    name = 'exist_spider'
    allowed_domains = ['exist.ru']
    end_point = 'http://exist.ru'
    start_urls = [
        end_point + 'cat/TecDoc/'
    ]

    search_regex_string = 'cat/TecDoc/\w+/(\w|\-|\%)+'

    rules = (
        Rule(
            LinkExtractor(
                allow=search_regex_string,
                deny_domains='m.exist.ru',
                deny=search_regex_string + '\?',
            ),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        sel = Selector(response)
         #todo: edit xpath
        models = sel.xpath('//tr[@onclick]').extract()

        for model in models:
            search_id = re.search("geturlEx\(\'(.+?)\'", model)
            if search_id:
                model_id = search_id.group(1)
                return Request(
                    url=response.url+'/'+model_id,
                    callback=self.parse_tree
                )

    def parse_tree(self, response):
        sel = Selector(response)
        parts_hrefs = sel.xpath('//*[@id="treeRoot"]//@href').extract()

        for href in parts_hrefs:
            in_starts = href.find("/cat/Parts.aspx")
            if in_starts != -1:
                href_last_part = href[in_starts:]

                return Request(
                    url=self.end_point + href_last_part,
                    callback=self.parse_parts
                )

    def parse_parts(self, response):
        print 'hi'
