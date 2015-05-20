# -*- coding: utf-8 -*-
import re
from scrapy import Selector, Request

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from auto_parker.items import Part


class ExistSpider(CrawlSpider):
    name = 'exist_spider'
    allowed_domains = ['exist.ru']
    end_point = 'http://exist.ru'

    start_urls = [
        end_point + '/cat/TecDoc/'
    ]

    search_regex_string = 'cat/TecDoc/Cars/Jaguar'

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
        models = response.selector.xpath('//tr[@onclick]')
        part = Part()

        for model in models:
            part['vehicle_brand'] = response.url.rsplit('/')[-2]
            part['vehicle_model'] = self.get_from_xpath(
                response.selector,
                '//*[@id="smBreadCrumbs"]/span[11]/text()'

            )
            params_sel = [
                ''.join(td.xpath('.//text()').extract())
                for td in Selector(text=model.extract()).xpath('//td')
                ]
            if params_sel:
                part['vehicle_modification'] = params_sel[0]
                part['vehicle_release_years'] = params_sel[-1]

            search_id = re.search("geturlEx\(\'(.+?)\'", model.extract())
            if search_id:
                model_id = search_id.group(1)
                request = self.form_part_request(
                    response.url+'/'+model_id,
                    self.parse_tree,
                    part
                )
                yield request

    def parse_tree(self, response):
        parts_hrefs = \
            response.selector.xpath('//*[@id="treeRoot"]//@href').extract()

        for href in parts_hrefs:
            in_starts = href.find("/cat/Parts.aspx")

            if in_starts != -1:
                href_last_part = href[in_starts:]
                request = self.form_part_request(
                    self.end_point + '/cat' + href_last_part,
                    self.parse_parts,
                    response.meta['part']
                )
                yield request

    def parse_parts(self, response):
        parts_table = response.selector.xpath('//table[@class="tbl"]/tr')

        if parts_table:
            parts = list()

            part_type = self.get_from_xpath(
                response.selector,
                '//td[@class="tabletitle"]/text()'
            )

            for part_in_table in parts_table[1:]:
                part = response.meta['part']

                part['type'] = part_type

                part['brand'] = self.get_from_xpath(
                    part_in_table,
                    '//div[@class="firmname"]/text()'
                )

                try:
                    part['art'] = self.get_from_xpath(
                        part_in_table,
                        '//div[@class="art"]/text()'
                    )
                except IndexError:
                    part['art'] = ''
                parts.append(part)

            return parts

    @staticmethod
    def get_from_xpath(sel, xpath_str, n=0):
        return sel.xpath(xpath_str).extract()[n]

    @staticmethod
    def form_part_request(url, callback, part):
        request = Request(
            url=url,
            callback=callback
        )
        request.meta['part'] = part
        return request

