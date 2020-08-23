import requests, sys
from bs4 import BeautifulSoup
import json



USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'


amazon_sorting = {
	'name': 'amazon',
	'sorting' : {
		'price_high_to_low': 'price-desc-rank',
		'price_low_to_high': 'price-asc-rank',
		'cust_reviews':'review-rank',
		'newest_arrivals':'date-desc-rank',
		'featured':'relevanceblender'	
	}
}

amazon_details = {
	'name':'amazon',
	'home_url': 'https://www.amazon.in',
	'search_url': 'https://www.amazon.in/s',
	'sorting' : amazon_sorting['sorting']
}


retailer_list = {
	'amazon':amazon_details
}


def get_item_list(search_items,retailer_name = 'amazon'):
	retailer = retailer_list[retailer_name]
	search_url = retailer['search_url']
	home_url = retailer['home_url']
	sort_by = retailer['sorting']['featured']
	search_items = search_items.strip()
	payload = {'k': search_items, 's': sort_by}
	headers = {'user-agent': USER_AGENT}
	res = requests.get(search_url,params=payload,headers=headers,timeout=5)
	if str(res.status_code).startswith('2') or str(res.status_code).startswith('3'):
		soup = BeautifulSoup(res.text,"lxml")
		html_code = res.text
		soup = BeautifulSoup(html_code,"lxml")
		all_res = []
		all_search_results = soup.select('div[data-component-type="s-search-result"]')
		for search_res in all_search_results:
			try:
				item_details_div = search_res.select_one('div.a-section.a-spacing-medium')
				item_image = item_details_div.select_one('span[data-component-type="s-product-image"] img').get('src')
				item_name = item_details_div.select_one('h2').get_text().strip()
				item_link = home_url + item_details_div.select_one('h2 a').get('href')
				item_price = item_details_div.select_one('span.a-price-whole').get_text()
				item_details = {
					"Item_Name" : item_name,
					"Item_Link" : item_link,
					"Item_Price" : item_price,
					"Item_Image" : item_image
				}
				all_res.append(item_details)
			except Exception as e:
				print(f"Error occurred:- {e}")
		all_res = json.dumps(all_res)
		return retailer_name, all_res, 'success'
	else:
		return retailer_name, [], 'error'

