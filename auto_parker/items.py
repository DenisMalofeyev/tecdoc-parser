import scrapy


class Part(scrapy.Item):
    part_type = scrapy.Field()
    part_brand = scrapy.Field()
    part_art = scrapy.Field()

    vehicle_brand = scrapy.Field()
