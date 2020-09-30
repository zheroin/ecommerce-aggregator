import requests, re
from bs4 import BeautifulSoup as BS

def amazon_price(url):
	headers = {
		"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
		}
	res = requests.get(url, headers=headers)
	soup = BS(res.content, "lxml")
	# print(soup.prettify())
	title = soup.select_one('#productTitle').get_text().strip()
	price = soup.select_one('#priceblock_ourprice').get_text()
	price = int(float(re.sub(r'[^0-9\.]', '', price)))
	return title,price
