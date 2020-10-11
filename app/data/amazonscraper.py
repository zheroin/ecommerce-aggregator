# -*- coding: utf-8 -*-
import scrapy, logging
from scrapy.utils.log import configure_logging
from urllib.parse import urlencode
try:
    from app.data.Items import MyItem
except (ModuleNotFoundError, ImportError) as e:
    # This is for the spidertester program
    from Items import MyItem
from flask import current_app

class AmazonscraperSpider(scrapy.Spider):
    name = 'amazonscraper'
    AMAZON_SEARCH = 'https://www.amazon.in/s?'

    # Default query string parameters
    params = {'ref':'nb_sb_noss'}

    def __init__(self, retailer_id, search_string=None, category_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_string = search_string
        self._amazon_params = AmazonscraperSpider.params
        self._amazon_params['k'] = self.search_string.strip()
        self.retailer_id = retailer_id
        self.category_name = category_name
        category_key = None
        if category_name == 'mobiles':
            category_key = {"rh" : "n:1805560031"}
            self._amazon_params.update(category_key)
        elif category_name == 'laptops':
            category_key = {"rh": "n:1375424031"}
            self._amazon_params.update(category_key)
        elif category_name == 'mensfashion':
            category_key = {"rh": "n:1968024031"}
            self._amazon_params.update(category_key)
        elif category_name == 'womensfashion':
            category_key = {"rh": "n:1968024031"}
            self._amazon_params.update(category_key)
        else:
            pass
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
        if self.category_name in ('laptops','mobiles'):
            all_results = response.xpath('//div[@data-component-type="s-search-result"]')
            logging.info("All results found. Looping through the results .... " if all_results else "No results found. Exiting")
            for res in all_results:
                item_details_div = res.xpath('(.//div[@class="a-section a-spacing-medium"])[1]')
                item_name = item_details_div.xpath('.//descendant::h2/a/span/text()').get()
                logging.info(f"Item name scraped ... {item_name}")
                item_image = item_details_div.xpath('.//descendant::img/@src').get()
                logging.info(f"Image scraped ... {item_image}")
                item_link = response.urljoin(item_details_div.xpath('.//descendant::h2/a/@href').get())
                logging.info(f"Item url scraped ... {item_link}")
                item_price = item_details_div.xpath('.//descendant::span[@class="a-price-whole"]/text()').get()
                logging.info(f"Item price scraped ... {item_price}")
                yield MyItem(retailer_id=self.retailer_id, item_name=item_name, item_image=item_image, item_url=item_link, item_price=item_price if item_price else 0)
        elif self.category_name in ('mensfashion','womensfashion'):
            all_results = response.xpath('//div[@class="a-section a-spacing-medium a-text-center"]')
            logging.info("All results found. Looping through the results .... " if all_results else "No results found. Exiting")
            for res in all_results:
                item_image = res.xpath('.//descendant::img/@src').get()
                logging.info(f"Image scraped ... {item_image}")
                item_link = response.urljoin(res.xpath('.//descendant::h2/a/@href').get())
                logging.info(f"URL scraped ... {item_link}")
                item_name = res.xpath('.//descendant::h2/a/span/text()').get()
                logging.info(f"Name scraped ... {item_name}")
                item_price = res.xpath('.//descendant::span[@class="a-price-whole"]/text()').get()
                logging.info(f"Price scraped ... {item_price}")
                yield MyItem(retailer_id=self.retailer_id, item_name=item_name, item_image=item_image, item_url=item_link, item_price=item_price if item_price else 0)

