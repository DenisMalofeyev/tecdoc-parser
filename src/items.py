import scrapy


class Part(scrapy.Item):
    mech_type = scrapy.Field()
    mech_brand = scrapy.Field()
    mech_mark = scrapy.Field()
    mech_modification = scrapy.Field()