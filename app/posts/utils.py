from app.models import Results, Items
from app.data import main
from app import db
import json

def get_search_results(search_string, category_name):
	"""
	in :- input the search string.
	output :- search id. Old search id if it is already present in DB, else new search ID after making entry to db
	"""
	result = Results.query.filter_by(search_string=search_string, category=category_name).order_by(Results.creation_date.desc()).first()
	result = None
	if result and len(result.items):
		# Verifying if the Items from the result list are present in the DB
		return result
	else:
		result = Results(search_string=search_string, category=category_name)
		db.session.add(result)
		db.session.commit()
		main(result=result)
	return result