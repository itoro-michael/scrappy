# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrackerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    found_url = scrapy.Field()
    title = scrapy.Field()
    website = scrapy.Field()
    description = scrapy.Field()
    description_source = scrapy.Field()
    block_rule = scrapy.Field()