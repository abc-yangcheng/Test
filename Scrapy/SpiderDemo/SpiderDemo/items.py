# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderdemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



#定义需要爬虫的item有哪些
class BookItem(scrapy.Item):
    author = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()