# -*- coding: utf-8 -*-
import scrapy, logging
from urllib.parse import urlencode
try:
    from app.data.Items import MyItem
except (ModuleNotFoundError, ImportError) as e:
    # This is for the spidertester program
    from Items import MyItem

class CromascraperSpider(scrapy.Spider):
    name = 'cromascraper'
    home_url = 'https://www.croma.com/'
    search_url = "https://www.croma.com/search/?"

    # Default query string parameters
    # params = {'otracker':'categorytree', 'sort':'popularity'}

    def __init__(self, retailer_id, search_string=None, category_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retailer_id = retailer_id
        self._params = {}
        self._params["text"] = f"{search_string.strip()}"
        search_url = self.search_url
        if category_name == 'mobiles':
            self._params["q"] = f"{search_string.strip()}:relevance:inStockFlag:true:category:95"
        elif category_name == 'laptops':
            self._params["q"] = f"{search_string.strip()}:relevance:inStockFlag:true:category:806:category:245:category:855:category:209:category:953:category:893"
        self._params = urlencode(self._params)
        self.url = f"{search_url}{self._params}"

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
        print("Getting croma data...")
        print("Response URL is {}".format(response.url))
        all_results = response.xpath('//div[@class="product__listing product__list" and @id="MM01030105"]/li')
        logging.info("All results found. Looping through the results .... " if all_results else "No results found. Exiting")
        print(f"Number of results found {len(all_results)}")
        for index, item_details_div in enumerate(all_results):
            item_name = item_details_div.xpath('.//descendant::h3/text()').get().strip('"')
            logging.info(f"Item name scraped ... {item_name}")
            item_image = item_details_div.xpath('.//descendant::a[@class="product__list--thumb"]/descendant::img/@data-src').get()
            logging.info(f"Image image scraped ... {item_image}")
            item_link = response.urljoin(item_details_div.xpath('.//descendant::a[@class="product__list--name"]/@href').get())
            logging.info(f"Item url scraped ... {item_link}")
            item_price = item_details_div.xpath('.//descendant::span[@class="pdpPrice"]/text()').get()
            logging.info(f"Item price scraped ... {item_price}")
            logging.info(f"Result {index}")
            yield MyItem(retailer_id=self.retailer_id, item_name=item_name, item_image=item_image, item_url=item_link, item_price=item_price if item_price else 0)
