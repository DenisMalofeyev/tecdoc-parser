import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request

from src.items import Part
from src.utils import get_from_xpath


class ExistSpider(CrawlSpider):
    name = 'exist_spider'
    allowed_domains = ['exist.ru']
    end_point = 'http://exist.ru'
    start_urls = [
        end_point + '/cat/TecDoc/'
    ]

    search_regex_string = 'cat/TecDoc/\w+/(\w|\-|\%)+'

    rules = (
        Rule(
            LinkExtractor(
                allow=search_regex_string,
                deny_domains='m.exist.ru',
                deny=search_regex_string + '\?',
            ),
            callback='parse_models',
            follow=True
        ),
    )

    def parse_models(self, response):
        models = response.selector.xpath('//tr[@onclick]').extract()

        for model in models:
            search_id = re.search("geturlEx\(\'(.+?)\'", model)

            if search_id:
                model_id = search_id.group(1)
                yield Request(
                    url=response.url+'/'+model_id,
                    callback=self.parse_tree
                )

    def parse_tree(self, response):
        parts_hrefs = \
            response.selector.xpath('//*[@id="treeRoot"]//@href').extract()

        for href in parts_hrefs:
            in_starts = href.find("/cat/Parts.aspx")

            if in_starts != -1:
                href_last_part = href[in_starts:]

                yield Request(
                    url=self.end_point + '/cat' + href_last_part,
                    callback=self.parse_parts
                )

    @staticmethod
    def parse_parts(response):
        parts_table = response.selector.xpath('//table[@class="tbl"]/tr')

        if parts_table:
            parts = list()

            vehicle_brand = get_from_xpath(
                response.selector,
                '//dl[@class="carInfo"]/dd/h3/text()'
            )

            part_type = get_from_xpath(
                response.selector,
                '//td[@class="tabletitle"]/text()'
            )

            for part_in_table in parts_table[1:]:
                part = Part()

                part['vehicle_brand'] = vehicle_brand
                part['part_type'] = part_type

                part['part_brand'] = get_from_xpath(
                    part_in_table,
                    '//div[@class="firmname"]/text()'
                )

                try:
                    part['part_art'] = get_from_xpath(
                        part_in_table,
                        '//div[@class="art"]/text()'
                    )
                except IndexError:
                    part['part_art'] = ''

                parts.append(part)

            return parts







