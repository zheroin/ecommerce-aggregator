from flask import render_template, Blueprint, flash, session, request, current_app
from app import db
from app.models import Items, TrackedItems
from app.posts.utils import get_search_results
from app.data.individual_price_scraper import amazon_price
import random, re

post = Blueprint('post',__name__)

@post.route('/search/<string:category_name>/<string:search_string>')
def search(category_name,search_string):
	"""
		Checks if the search string is present in database. Displays the results off the database if presents, else scrapes the data off the website and adds to database.
	"""
	search_string = search_string.lower().strip()
	result = get_search_results(search_string)
	current_app.logger.info(f"Search id {result.id}")
	all_results = result.items
	random.shuffle(all_results)
	return render_template('search.html',results = all_results,search_str=search_string, search_id = result.id)

# @post.route('/add_to_watchlist',methods=['POST'])
# def watch():
# 	item_id, user_id, desired_price = [request.json[k] for k in ('item_id', 'user_id' , 'desired_price')]
# 	desired_price = int(float(re.sub(r'[^0-9\.]', '', desired_price)))
# 	print(f"User ID {user_id}")
# 	print(f"Session User ID {session['user_id']}")
# 	try:
# 		if int(user_id) != int(session['user_id']):
# 			raise AttributeError("User ID does not match")
# 		# Add item to tracked items table and scrape the current price.
# 		item_url = Items.query.filter_by(id=item_id).first().item_url
# 		title, price = amazon_price(item_url)
# 		tracked_item = TrackedItems.query.filter(TrackedItems.item_url == item_url).first()
# 		if tracked_item:
# 			if tracked_item.current_price != price:
# 			# Price has changed so update the record with new price
# 				tracked_item.current_price = price
# 				tracked_item.desired_price = desired_price
# 		else:
# 			tracked_item = TrackedItems(user_id = user_id, item_url = item_url, item_name = title, current_price = price, desired_price = desired_price)
# 			db.session.add(tracked_item)
# 		db.session.commit()
# 		print("Item added to watchlist")
# 		return {"message": "successfully added"}, 201
# 	except Exception as e:
# 		current_app.logger.info("Exception - {}".format(e))
# 		return {"error": "Errored out"}, 400

@post.route('/add_to_watchlist',methods=['POST'])
def watch():
	# Desired price has to be formatted into an integer
	# item_id, user_id, desired_price = [request.json[k] for k in ('item_id', 'user_id' , 'desired_price')]
	item_id = 22
	user_id = 1
	desired_price = 80000

	# Add item to tracked items table and scrape the current price.
	item_url = Items.query.filter_by(id=item_id).first().item_url
	title, price = amazon_price(item_url)
	tracked_item = TrackedItems.query.filter(TrackedItems.item_url == item_url).first()
	if tracked_item:
		if tracked_item.current_price != price:
			# Price has changed so update the record with new price
			tracked_item.current_price = price
			tracked_item.desired_price = desired_price
	else:
		tracked_item = TrackedItems(user_id = user_id, item_url = item_url, item_name = title, current_price = price, desired_price = desired_price)
		db.session.add(tracked_item)
	db.session.commit()
	print("Item added to watchlist")
	return {"message":"Added to watchlist"}