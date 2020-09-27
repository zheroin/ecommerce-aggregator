# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.log import configure_logging
import urllib
import datetime, logging
from urllib.parse import urlencode, quote_plus
from .Items import MyItem
from app.models import Categories, shop_category, Retailer
from app import db
from flask import current_app

class AmazonscraperSpider(scrapy.Spider):
    ## Uncomment incase there are any issues.
    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO
    # )
    name = 'amazonscraper'
    AMAZON_SEARCH = 'https://www.amazon.in/s?'
    amazon_params = {'s':'relevance-blender', 'ref':'nb_sb_noss'}

    def __init__(self, retailer_id=1, search_string=None, category_name=None, *args, **kwargs):
        super(AmazonscraperSpider, self).__init__(*args, **kwargs)
        self.search_string = search_string
        self._amazon_params = AmazonscraperSpider.amazon_params
        self.retailer_id = retailer_id
        category_key = None
        # if category_name == 'mobiles':
        #     category_key = {"rh" : "n:1389401031"}
        if category_name == 'laptops':
            category_key = {"rh":"n:1375424031"}
            self._amazon_params.update(category_key)
        self._amazon_params['k'] = self.search_string.strip()
        self._amazon_params = urlencode(self._amazon_params)
        amazon_url = f"{self.AMAZON_SEARCH}{self._amazon_params}"
        self.url = amazon_url

    def start_requests(self):
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        # "Host": "httpbin.org",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        }
        yield scrapy.Request(url=self.url, callback=self.parse, headers=headers)

    def parse(self, response):
        print("Getting amazon data...")
        print("Response URL is {}".format(response.url))
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
            yield MyItem(retailer_id=self.retailer_id, item_name=item_name, item_image=item_image, item_url=item_link, item_price=item_price if item_price else 0)