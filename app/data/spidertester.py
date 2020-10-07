import crochet
crochet.setup()
import scrapy
from scrapy import signals
from scrapy.crawler import  CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
# Importing all spiders
from amazonscraper import AmazonscraperSpider
from flipkartscraper import FlipkartscraperSpider
from cromascraper import CromascraperSpider
from paytmscraper import PaytmscraperSpider

output_data=[]

retailer_details = {}

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
configure_logging(s)

crawl_runner = CrawlerRunner(s)

@crochet.run_in_reactor
def scrape_amazon_with_crochet(retailer_id, search_string, category_name):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    print(f"Amazon retailer ID {retailer_id}")
    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = crawl_runner.crawl(AmazonscraperSpider, retailer_id = retailer_id, search_string = search_string, category_name=category_name)
    return eventual

@crochet.run_in_reactor
def scrape_flipkart_with_crochet(retailer_id, search_string, category_name):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    print(f"Flipkart retailer ID {retailer_id}")
    eventual = crawl_runner.crawl(FlipkartscraperSpider, retailer_id = retailer_id, search_string = search_string, category_name=category_name)
    return eventual

@crochet.run_in_reactor
def scrape_croma_with_crochet(retailer_id, search_string, category_name):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    print(f"Croma retailer ID {retailer_id}")
    eventual = crawl_runner.crawl(CromascraperSpider, retailer_id = retailer_id, search_string = search_string, category_name=category_name)
    return eventual

@crochet.run_in_reactor
def scrape_paytm_with_crochet(retailer_id, search_string, category_name):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(PaytmscraperSpider, retailer_id = retailer_id, search_string = search_string, category_name=category_name)
    return eventual

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))

def main(category_name, search_string):
    all_eventuals = []
    try:
        all_eventuals.append(scrape_amazon_with_crochet(retailer_id=1,search_string=search_string , category_name=category_name))
        # all_eventuals.append(scrape_flipkart_with_crochet(retailer_id=2, search_string=search_string , category_name=category_name))
        # all_eventuals.append(scrape_paytm_with_crochet(retailer_id=9, search_string=search_string , category_name=category_name))
        if category_name == 'laptops' or category_name == 'mobiles':
            all_eventuals.append(scrape_croma_with_crochet(retailer_id=3, search_string=search_string , category_name=category_name))
            # Query all the categories here. Get the key for each shop in the spider calling functions
            # Scrape Croma
            if 'asus' in search_string.lower():
                # Scrape asus online store
                pass
            elif 'hp' in search_string.lower():
                # Scrape hp online store
                pass
        elif category_name == 'mensfashion':
            pass
        elif category_name == "womensfashion":
            pass
            # scrape myntra, jabong, shein
        for eventual in all_eventuals:
            eventual.wait(timeout=15)
        num = 0
        for index, i in enumerate(output_data):
            item_name = i['item_name']
            retailer_id = i['retailer_id']
    except crochet.TimeoutError:
        pass
    else:
        print(f"Web scraping output count -")
        print(f"{num} New distinct items added to DB..")
    finally:
        # Clear the output data list, to avoid mix ins with other results.
        output_data.clear()
        num = 0

main("womensfashion","salwar kameez")