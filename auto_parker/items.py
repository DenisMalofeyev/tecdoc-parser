# -*- coding: utf-8 -*-
import scrapy


class Part(scrapy.Item):
    type = scrapy.Field()
    brand = scrapy.Field()
    art = scrapy.Field()
    # category = scrapy.Field()

    vehicle_brand = scrapy.Field()
    vehicle_model = scrapy.Field()
    vehicle_modification = scrapy.Field()
    vehicle_engine_type = scrapy.Field()
    vehicle_engine_model = scrapy.Field()
    vehicle_engine_volume = scrapy.Field()
    vehicle_power = scrapy.Field()
    vehicle_drive = scrapy.Field()
    vehicle_kpp_type = scrapy.Field()
    vehicle_doors = scrapy.Field()
    vehicle_release_years = scrapy.Field()