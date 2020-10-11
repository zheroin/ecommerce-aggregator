import requests, re
from bs4 import BeautifulSoup as BS
from dataclasses import dataclass

@dataclass
class IndividualScraper:
	mapping = {
		'amazon':'cmd_amazon_price',
		'flipkart': 'cmd_flipkart_price',
		'paytm':'cmd_paytm_price',
		'croma':'cmd_croma_price'
		}

	def cmd_amazon_price(self, soup):
		title = soup.select_one('#productTitle').get_text().strip()
		price = soup.select_one('#priceblock_ourprice').get_text()
		price = int(float(re.sub(r'[^0-9\.]', '', price)))
		return (title,price)

	def cmd_flipkart_price(self, soup):
		title = soup.select_one('._35KyD6').get_text().strip()
		price = soup.select_one('._1vC4OE._3qQ9m1').get_text()
		price = int(float(re.sub(r'[^0-9\.]', '', price)))
		return (title,price)

	def cmd_paytm_price(self, soup):
		title = soup.select_one('h1').get_text().strip()
		price = soup.select_one('._1V3w').get_text()
		price = int(float(re.sub(r'[^0-9\.]', '', price)))
		return (title,price)

	def cmd_croma_price(self, soup):
		title = soup.select_one('h1').get_text().strip()
		price = soup.select_one('.pdpPrice').get_text()
		price = int(float(re.sub(r'[^0-9\.]', '', price)))
		return (title,price)

	def send_request(self,url):
		headers = {
		"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
		}
		res = requests.get(url, headers=headers)
		if not res.ok:
			raise IndexError
		soup = BS(res.content, "lxml")
		return soup


	def get_price(self, url):
		soup = self.send_request(url)
		func_name = None
		try:
			url_domain = re.findall(r"//(.*?)/", url)[0]
			for name in self.mapping.keys():
				if name in url_domain.lower():
					func_name = self.mapping[name]
			func = getattr(self, f'{func_name}', None)
			if not func:
				raise IndexError
			else:
				return func(soup)
		except IndexError:
			raise ValueError("Invalid URL")
		except Exception as e:
			raise ValueError(f"Errored out {e}")
