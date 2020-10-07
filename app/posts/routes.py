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
	result = get_search_results(search_string, category_name)
	current_app.logger.info(f"Search id {result.id}")
	all_results = result.items
	random.shuffle(all_results)
	return render_template('search.html',results = all_results,category=category_name, search_str=search_string, search_id = result.id)

@post.route('/compare_cart', methods=['POST', 'DELETE'])
def compare_cart():
	data = request.json
	try:
		if request.method == 'POST':
			if not data:
				raise ValueError("JSON data not provided")
			item_id = data.get('item_id')
			if not item_id:
				raise ValueError("Item ID is not provided")
			if 'cart' in session:
				cart_list = session['cart']
				if not item_id in session['cart']:
					cart_list.append(item_id)
					session['cart'] = list(set(cart_list))
			else:
			# In this block, the user has not started a cart, so we start it for them and add the product. 
				# session['cart'] = set()
				session['cart'] = [item_id]
			return {"message": "Successfully added to cart"}, 200
		else:
			if not data:
				# Deleting entire cart
				session.pop('cart', None)
			else:
				item_id = data.get('item_id')
				# Deleting single item from cart
				cart_list = session['cart']
				try:
					cart_list.remove(item_id)
				except ValueError:
					pass
				else:
					session['cart'] = cart_list
			return {"message": "successfully deleted"}, 200
	except Exception as e:
		current_app.logger.info(f"Errored out. {e}")
		return {"error": f"Errored out. {e}"}, 400


@post.route('/watchlist',methods=['POST', 'PUT', 'DELETE'])
def watch():
	# Desired price has to be formatted into an integer

	if request.method == 'POST':
		# item_id, user_id, desired_price = [request.json[k] for k in ('item_id', 'user_id' , 'desired_price')]
		item_id = 22
		user_id = 1
		desired_price = 80000

		tracked_item = TrackedItems.query.filter(TrackedItems.search_item_id == item_id, TrackedItems.user_id == user_id).first()
		if not tracked_item:
			# Add item to tracked items table and scrape the current price.
			item = Items.query.filter_by(id=item_id).first()
			tracked_item = TrackedItems(user_id = user_id,
				item_url = item.item_url,
				item_name = item.item_name,
				current_price = item.item_price,
				desired_price = desired_price)
			db.session.add(tracked_item)
			db.session.commit()
			return {"message" : "Item added to track list"}, 201
	elif request.method == 'PUT':
		tracked_item_id, user_id, new_desired_price = [request.json[k] for k in ('tracked_item_id', 'user_id' , 'new_desired_price')]
		tracked_item = TrackedItems.query.filter(TrackedItems.id == tracked_item_id, TrackedItems.user_id == user_id).first()
		if tracked_item:
			tracked_item.desired_price = new_desired_price
			db.session.commit()
			return {"message" : "Tracked item is updated"}, 200
		return {"error": "No tracked item for the details provided. Please create a new one."}, 400
	else:
		tracked_item_id, user_id = [request.json[k] for k in ('tracked_item_id', 'user_id' )]
		tracked_item = TrackedItems.query.filter(TrackedItems.id == tracked_item_id, TrackedItems.user_id == user_id).first()
		if tracked_item:
			db.session.delete(tracked_item)
			db.session.commit()
			return {"message" : "Tracked item is deleted"}, 200
		return {"error": "No tracked item for the details provided. Please create a new one."}, 400