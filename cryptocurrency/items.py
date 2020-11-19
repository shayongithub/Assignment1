# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CryptocurrencyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    A_DATE = scrapy.Field()
    B_OPEN = scrapy.Field()
    C_HIGH = scrapy.Field()
    D_LOW = scrapy.Field()
    E_CLOSE = scrapy.Field()
    F_VOLUME = scrapy.Field()
    H_MARKETCAP = scrapy.Field()
    pass
