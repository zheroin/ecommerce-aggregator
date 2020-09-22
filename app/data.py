from requests_html import HTMLSession, AsyncHTMLSession
from flask import current_app
from multiprocessing import Process
from threading import Thread
from app.models import Items
from app import db
import time

def get_fp(search_string, search_id):
  session = HTMLSession()
  url = "https://www.flipkart.com/search"
  payload = {'q': search_string.strip()}
  res = session.get(url, params=payload, timeout=5)
  # await res.html.arender(scrolldown=20, sleep=.1)
  all_res_sel = '#container > div > div.t-0M7P._2doH3V > div._3e7xtJ > div._1HmYoV.hCUpcT > div:nth-child(2)'
  all_results = res.html.find(all_res_sel, first=True)
  items = all_results.find('._1UoZlX')
  all_items_list = []
  current_app.logger.info("Getting flipkart data ....")
  for item in items:
    try:
      item_link = (x for x in item.find('a', first=True).absolute_links).__next__()
      item_name = item.find('._3wU53n', first=True).text
      item_price = item.find('div._1vC4OE._2rQ-NK', first=True).text
      all_images = item.find('div._3BTv9X img')
      item_image = [i.attrs.get('src') for i in all_images][0]
      all_items_list.append({
          'name':item_name, 
          'price': item_price, 
          'image': item_image, 
          'link' : item_link,
          'retailer':'flipkart' })
      current_app.logger.info(item_name[:10])
      i = Items(search_id = search_id, item_name = item_name, item_url = item_link, item_price = item_price, item_image = item_image)
      db.session.add(i)
    except Exception as e:
      current_app.logger.info(f'Exception while extracting flipkart data - {e}')
  current_app.logger.info("Flipkart count {}".format(len(all_items_list)))
  db.session.commit()
  return 

def get_az(search_string, search_id):
  session = HTMLSession()
  url = 'https://www.amazon.in/s'
  payload = {'k': search_string.strip(),'s':'relevanceblender' }
  res = session.get(url, params=payload, timeout=5)
  all_results = res.html.find('div[data-component-type="s-search-result"]')
  all_items_list = []
  current_app.logger.info("Getting amazon data ....")
  for r in all_results:
    try:
      item_details_div = r.find('div.a-section.a-spacing-medium', first=True)
      item_name = item_details_div.find('h2', first=True).text
      item_image = item_details_div.find('span[data-component-type="s-product-image"] img', first=True).attrs.get('src')
      item_link = (x for x in item_details_div.find('h2 a', first=True).absolute_links).__next__()
      item_price = item_details_div.find('span.a-price-whole', first=True).text
      item_details = {
          "name" : item_name,
          "link" : item_link,
          "price" : item_price,
          "image" : item_image,
          "retailer": "amazon"
          }
      all_items_list.append(item_details)
      current_app.logger.info(item_name[:10])
      i = Items(search_id = search_id, item_name = item_name, item_url = item_link, item_price = item_price, item_image = item_image)
      db.session.add(i)
    except Exception as e:
      current_app.logger.info(f'Exception while extracting amazon data - {e}')
  db.session.commit()
  current_app.logger.info("Amzon count {}".format(len(all_items_list)))
  return  

def gen_data(search_str, search_id):
  get_az(search_str, search_id)
  get_fp(search_str, search_id)
