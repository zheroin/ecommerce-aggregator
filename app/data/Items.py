import scrapy, re
# Scrapy Item used by all spiders

class MyItem(scrapy.Item):
    retailer_id = scrapy.Field()
    item_name = scrapy.Field()
    item_price = scrapy.Field()
    item_image = scrapy.Field()
    item_url = scrapy.Field()

    def __init__(self, *args,**kwargs):
        strip_chars = '\'"!?@#$. '
        new_params = {}
        for key, val in kwargs.items():
            new_val = val
            if key == 'item_name':
                new_val = val.strip(strip_chars)
            elif key == 'item_price':
                new_val = int(float(re.sub(r"[^\d.]","", val)))
            new_params[key] = new_val
        super().__init__(*args,**new_params)
