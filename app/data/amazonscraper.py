# -*- coding: utf-8 -*-
import scrapy
import urllib
import datetime, logging
from urllib.parse import urlencode, quote_plus
from .Items import MyItem
from app.models import Categories, shop_category, Retailer
from app import db

class AmazonscraperSpider(scrapy.Spider):
    name = 'amazonscraper'
    AMAZON_HOME = 'https://www.amazon.in/'
    AMAZON_SEARCH = 'https://www.amazon.in/s?'
    amazon_params = {'s':'relevance-blender', 'ref':'nb_sb_noss'}

    @property
    def retailer_id(self):
        ret = Retailer.query.filter(Retailer.name=='amazon').first()
        if ret:
            return ret.id

    def __init__(self, search_string=None, category_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_string = search_string
        self._amazon_params = AmazonscraperSpider.amazon_params
        category_key = None
        if category_name == 'laptops':
            category_key = {"rh":"n:1375424031"}
            self._amazon_params.update(category_key)
        # try:
        #     category_id = Categories.query.filter(Categories.name == category_name).first().id # Getting the category ID
        #     retailer_id = Retailer.query.filter(Retailer.name == 'amazon').first().id
        #     category_key = db.session.query(shop_category).\
        #         filter(shop_category.category_id == category_id, shop_category.retailer_id == retailer_id).\
        #             first().cat_url_key
        # except Exception as e:
        #     print("Error {}".format(e))
        self._amazon_params['k'] = self.search_string.strip()
        self._amazon_params = urlencode(self._amazon_params)
        amazon_url = f"{self.AMAZON_SEARCH}{self._amazon_params}"
        self.url = amazon_url
        # self.url = "https://www.amazon.in/s?k=acer+laptops&rh=n%3A1375424031&s=relevance-blender&ref=nb_sb_noss"

    def start_requests(self):
        print("In start requests")
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Host": "httpbin.org",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        }
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        print("Getting amazon data...")
        print(f"URL {response.url}")
        all_results = response.xpath('//div[@data-component-type="s-search-result"]')
        print(len(all_results))
        print("All results found. Looping through the results .... " if all_results else "No results found. Exiting")
        for res in all_results:
            item_details_div = res.xpath('(.//div[@class="a-section a-spacing-medium"])[1]')
            item_name = item_details_div.xpath('.//descendant::h2/a/span/text()').get()
            print(f"Item name scraped ... {item_name}")
            item_image = item_details_div.xpath('.//descendant::img/@src').get()
            print(f"Image URL scraped ... {item_image}")
            item_link = response.urljoin(item_details_div.xpath('.//descendant::h2/a/@href').get())
            print(f"Item url scraped ... {item_link}")
            item_price = item_details_div.xpath('.//descendant::span[@class="a-price-whole"]/text()').get()
            print(f"Item price scraped ... {item_price}")
            yield MyItem(retailer_id=self.retailer_id, item_name=item_name, item_image=item_image, item_url=item_link, item_price=item_price if item_price else 0)

