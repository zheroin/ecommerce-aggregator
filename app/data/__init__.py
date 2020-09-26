# from flask import current_app
from app import db
import time
import crochet, time
crochet.setup()
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from .amazonscraper import AmazonscraperSpider


output_data = []
settings = {
    'FEED_EXPORT_ENCODING' :'utf-8',
    'USER_AGENT' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'COOKIES_ENABLED' : False,
    'LOG_STDOUT' : True
}

s = get_project_settings()

s.update({
    'FEED_EXPORT_ENCODING' :'utf-8',
    'USER_AGENT' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'COOKIES_ENABLED' : False,
    "LOG_ENABLED": True,
    'LOG_STDOUT' : True
})

# init the logger using setting
# configure_logging(s)

crawl_runner = CrawlerRunner(s)

even_set = set()

@crochet.run_in_reactor
def scrape_amazon_with_crochet(search_string, category_name, retailer_id=1):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = crawl_runner.crawl(AmazonscraperSpider, search_string = search_string, category_name=category_name)
    return eventual

@crochet.run_in_reactor
def scrape_flipkart_with_crochet(search_string, category_name, retailer_id=2):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    eventual = crawl_runner.crawl(AmazonscraperSpider, search_string = search_string, category_name=category_name)
    return eventual


#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))

def main(search_id, search_string, category_name):
  from app.models import Items
  all_eventuals = []
  try:
    if category_name == 'laptops':
        # Query all the categories here. Get the key for each shop in the spider calling functions
        all_eventuals.append(scrape_amazon_with_crochet(search_string=search_string , category_name=category_name, retailer_id=1))
    for eventual in all_eventuals:
        eventual.wait(timeout=15)
    for i in output_data:
        item = Items.create_item(search_id=search_id, **i)
        db.session.add(item)
  except crochet.TimeoutError:
    pass
  db.session.commit()

