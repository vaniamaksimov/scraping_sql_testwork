# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NedradvItem(scrapy.Item):
    auction_site_id = scrapy.Field()
    auction_area = scrapy.Field()
    auction_region = scrapy.Field()
    auction_status = scrapy.Field()
    auction_date = scrapy.Field()
    auction_deadline = scrapy.Field()
    auction_patricipation_fee = scrapy.Field()
    auction_holder = scrapy.Field()
