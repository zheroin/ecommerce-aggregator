# -*- coding: utf-8 -*-
import scrapy, logging, re, json
from scrapy.utils.log import configure_logging
from urllib.parse import urlencode
try:
    from app.data.Items import MyItem
except (ModuleNotFoundError, ImportError) as e:
    # This is for the spidertester program
    from Items import MyItem

class FlipkartscraperSpider(scrapy.Spider):
    name = 'flipkartscraper'
    FLIPKART_HOME = 'https://www.flipkart.com'
    FLIPKART_SEARCH = "https://www.flipkart.com/search?"

    # Default query string parameters
    params = {'otracker':'categorytree', 'sort':'popularity'}

    def __init__(self, retailer_id, search_string=None, category_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_string = search_string
        self._params = FlipkartscraperSpider.params
        self.retailer_id = retailer_id
        self._params["q"] = self.search_string.strip()
        category_key = None
        search_url = None
        if category_name == 'mobiles':
            search_url = "https://www.flipkart.com/mobiles/pr?"
            category_key = {"sid":"tyy,4io"}
            self._params.update(category_key)
        elif category_name == 'laptops':
            search_url = "https://www.flipkart.com/computers/laptops/pr?"
            category_key = {"sid":"6bo,b5g"}
            self._params.update(category_key)
        else:
            search_url = self.FLIPKART_SEARCH
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
        print("Getting flipkart data...")
        print("Response URL is {}".format(response.url))
        pattern = r"listingId\":\"([a-zA-Z0-9]+?)\",\"media\":\{\"images\":.+?\"url\":\"(http:[^\s]+?\.jpeg{1}\?q=\{@quality\})"

        # Getting the list of dynamically generated image thumbnails
        js = response.xpath('//script[@id="is_script"]').re(pattern)
        try:
            js_dict = {js[i] : js[i + 1].replace("{@width}", '312').replace('{@height}', '312').replace('{@quality}','70') for i in range(0, len(js), 2) }
        except IndexError:
            pass
        # print(js_dict)
        all_results = response.xpath('(//div[@class="_1HmYoV _35HD7C"])[2]/div[@class="bhgxx2 col-12-12"]/div[@class="_3O0U0u"]')
        logging.info("All results found. Looping through the results .... " if all_results else "No results found. Exiting")
        for res in all_results:
            item_details_div = res.xpath('.//descendant::div[@class="_1UoZlX"]')
            item_name = item_details_div.xpath('.//descendant::div[@class="_3wU53n"]/text()').get()
            logging.info(f"Item name scraped ... {item_name}")
            item_link = response.urljoin(item_details_div.xpath('.//a/@href').get())
            logging.info(f"Item url scraped ... {item_link}")
            listing_id = re.findall(r"lid=(.+?)&", item_link)[0]
            item_image = js_dict.get(listing_id)
            logging.info(f"Image URL scraped ... {item_image}")
            item_price = item_details_div.xpath('.//descendant::div[@class="_1vC4OE _2rQ-NK"]/text()').get()
            logging.info(f"Item price scraped ... {item_price}")
            yield MyItem(retailer_id=self.retailer_id, item_name=item_name, item_image=item_image, item_url=item_link, item_price=item_price if item_price else 0)
