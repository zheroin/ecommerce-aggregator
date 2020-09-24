# -*- coding: utf-8 -*-
import scrapy
import urllib
import datetime, logging
from urllib.parse import urlencode, quote_plus

class MyItem(scrapy.Item):
    shop = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    link = scrapy.Field()

class AmazonscraperSpider(scrapy.Spider):
    name = 'amazonscraper'
    HOME_URL = 'https://www.amazon.in/'
    SEARCH_URL = 'https://www.amazon.in/s'
    start_urls = []

    def __init__(self, search_string=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_string = search_string
        amazon_params = urlencode({ 's': 'price-asc-rank', 'k': self.search_string.strip(), 'ref' : 'nb_sb_noss'}, quote_via=quote_plus)
        amazon_url = f"{self.SEARCH_URL}?%s" % amazon_params
        self.start_urls.append(amazon_url)
        flipkart_params = urlencode({'q': self.search_string.strip()}, quote_via=quote_plus)
        flipkart_url = f"https://www.flipkart.com/search?{flipkart_params}"
        self.start_urls.append(flipkart_url)

    def parse(self, response):
        print(response.request.headers)
        if 'amazon' in response.url:
            print("Getting amazon data...")
            all_results = response.xpath('//div[@data-component-type="s-search-result"]')
            logging.info("All results found. Looping through the results .... " if all_results else "No results found. Exiting")
            for res in all_results:
                item_details_div = res.xpath('(.//div[@class="a-section a-spacing-medium"])[1]')
                item_name = item_details_div.xpath('.//descendant::h2/a/span/text()').get()
                logging.info(f"Item name scraped ... {item_name}")
                item_image = item_details_div.xpath('.//descendant::img/@src').get()
                logging.info(f"Image URL scraped ... {item_image}")
                item_link = response.urljoin(item_details_div.xpath('.//descendant::h2/a/@href').get())
                logging.info(f"Item url scraped ... {item_link}")
                item_price = item_details_div.xpath('.//descendant::span[@class="a-price-whole"]/text()').get()
                logging.info(f"Item price scraped ... {item_price}")
                yield MyItem(shop="amazon", name=item_name, image=item_image, link=item_link, price=item_price)
