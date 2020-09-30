# -*- coding: utf-8 -*-
import scrapy, logging
from urllib.parse import urlencode
try:
    from app.data.Items import MyItem
except (ModuleNotFoundError, ImportError) as e:
    # This is for the spidertester program
    from Items import MyItem

class PaytmscraperSpider(scrapy.Spider):
    name = 'paytmscraper'
    home_url = 'https://paytmmall.com/'
    search_url = "https://paytmmall.com/shop/search?"

    # Default query string parameters
    params = {'from':'organic', 'child_site_id':'6', 'site_id':'2'}

    def __init__(self, retailer_id, search_string=None, category_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retailer_id = retailer_id
        self._params = PaytmscraperSpider.params
        self._params["q"] = f"{search_string.strip()}"
        search_url = self.search_url
        if category_name == 'mobiles':
            self._params["category"] = f"6224"
        elif category_name == 'laptops':
            self._params["category"] = f"6453"
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
        print("Getting paytm mall data...")
        print("Response URL is {}".format(response.url))
        all_results = response.xpath('//div[@class="_1LZ3"]/descendant::div[@class="_3WhJ"]')
        logging.info("All results found. Looping through the results .... " if all_results else "No results found. Exiting")
        print(f"Number of results found {len(all_results)}")
        for index, item_details_div in enumerate(all_results):
            item_name = item_details_div.xpath('.//a/descendant::div[@class="UGUy"]/text()').get().strip('"')
            logging.info(f"Item name scraped ... {item_name}")
            item_image = item_details_div.xpath('.//a/div[@class="_3nWP"]/img/@src').get()
            logging.info(f"Image image scraped ... {item_image}")
            item_link = response.urljoin(item_details_div.xpath('.//a/@href').get())
            logging.info(f"Item url scraped ... {item_link}")
            item_price = item_details_div.xpath('.//a/descendant::div[@class="_1kMS"]/span/text()').get()
            logging.info(f"Item price scraped ... {item_price}")
            yield MyItem(retailer_id=self.retailer_id, item_name=item_name, item_image=item_image, item_url=item_link, item_price=item_price if item_price else 0)
