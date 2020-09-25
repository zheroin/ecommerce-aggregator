import scrapy
# Scrapy Item used by all spiders
class MyItem(scrapy.Item):
    retailer_id = scrapy.Field()
    item_name = scrapy.Field()
    item_price = scrapy.Field()
    item_image = scrapy.Field()
    item_url = scrapy.Field()
