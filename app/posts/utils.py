from app.models import Results, Items
from app.generate_data.amazon import get_item_list
from app import db
import json

def get_search_results(search_string, retailer):
	"""
	in :- input the search string.
	output :- search id. Old search id if it is already present in DB, else new search ID after making entry to db
	"""
	result = Results.query.filter_by(search_string=search_string,retailer_name=retailer).order_by(Results.last_update_date.desc()).first()
	if result:
		# Verifying if the Items from the result list are present in the DB
		if Items.query.filter_by(search_id = result.id).count() > 0:
			return result.id
		else:
			# Updating the existing record, incase there are no items in the result list
			retailer, res_in_json, status_code = get_item_list(search_items = search_string)
			res_list = json.loads(res_in_json)
			result = Results(search_string=search_string, retailer_name=retailer)
			db.session.add(result)
			db.session.commit()
			
			for item in res_list:
				i = Items(search_id = result.id, item_name = item['Item_Name'], item_url = item['Item_Link'], item_price = item['Item_Price'], item_image = item['Item_Image'])
				db.session.add(i)
			db.session.commit()
	else:
		# Inserting into the database
		retailer, res_in_json, status_code = get_item_list(search_items = search_string)
		res_list = json.loads(res_in_json)
		result = Results(search_string=search_string, retailer_name=retailer)
		db.session.add(result)
		db.session.commit()
		for item in res_list:
			i = Items(search_id = result.id, item_name = item['Item_Name'], item_url = item['Item_Link'], item_price = item['Item_Price'], item_image = item['Item_Image'])
			db.session.add(i)
		db.session.commit()
	return result.id