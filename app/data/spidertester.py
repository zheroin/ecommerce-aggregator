import crochet, time
crochet.setup()
import scrapy
from scrapy import signals
from scrapy.crawler import  CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from amazonscraper import AmazonscraperSpider
from flipkartscraper import FlipkartscraperSpider
from cromascraper import CromascraperSpider
from paytmscraper import PaytmscraperSpider
from scrapy.utils.log import configure_logging


output_data=[]

s = get_project_settings()

s.update({
    'FEED_EXPORT_ENCODING' :'utf-8',
    'USER_AGENT' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'COOKIES_ENABLED' : False,
    "LOG_ENABLED": True,
    'LOG_STDOUT' : True
})

# init the logger using setting
# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
configure_logging(s)

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO
    # )

crawl_runner = CrawlerRunner(s)
@crochet.run_in_reactor
def scrape_amazon_with_crochet(search_string, category_name):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    # with current_app.app_context():
    #     retailer_id = Retailer.query.filter_by(name="amazon").first().id
    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = crawl_runner.crawl(AmazonscraperSpider, retailer_id = 1, search_string = search_string, category_name=category_name)
    return eventual

@crochet.run_in_reactor
def scrape_flipkart_with_crochet(search_string, category_name):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    # with current_app.app_context():
    #     retailer_id = Retailer.query.filter_by(name="flipkart").first().id
    eventual = crawl_runner.crawl(FlipkartscraperSpider, retailer_id = 2, search_string = search_string, category_name=category_name)
    return eventual

@crochet.run_in_reactor
def scrape_croma_with_crochet(search_string, category_name):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    # with current_app.app_context():
    #     retailer_id = Retailer.query.filter_by(name="flipkart").first().id
    eventual = crawl_runner.crawl(FlipkartscraperSpider, retailer_id = 2, search_string = search_string, category_name=category_name)
    return eventual

@crochet.run_in_reactor
def scrape_paytm_with_crochet(search_string, category_name):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    eventual = crawl_runner.crawl(PaytmscraperSpider, retailer_id = 3, search_string = search_string, category_name=category_name)
    return eventual

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))
    print("Added to the result")

def test_runner(category_name, search_string):
  all_eventuals = []
  try:
    if category_name == 'laptops' or category_name == 'mobiles':
        # Query all the categories here. Get the key for each shop in the spider calling functions
        # all_eventuals.append(scrape_amazon_with_crochet(search_string=search_string , category_name=category_name))
        all_eventuals.append(scrape_flipkart_with_crochet(search_string=search_string , category_name=category_name))
        # all_eventuals.append(scrape_croma_with_crochet(search_string=search_string , category_name=category_name))
    for eventual in all_eventuals:
        eventual.wait(timeout=15)
    # for index, i in enumerate(output_data):
    #     item_name = i['item_url']
    #     print(f"Index {index} Shop - {i['retailer_id']} name - {item_name}")
  except crochet.TimeoutError:
    pass
  finally:
    # Clear the output data list, to avoid mix ins with other results.
    output_data.clear()

test_runner("mobiles","redmi")