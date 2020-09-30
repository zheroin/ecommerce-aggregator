from flask import render_template, Blueprint, flash, redirect, url_for, session
from app.posts.forms import SearchForm
from app.models import Items
from app import db

main = Blueprint('main',__name__)

@main.route('/',methods=['GET','POST'])
@main.route('/home.html',methods=['GET','POST'])
@main.route('/home',methods=['GET','POST'])
def home():
	form = SearchForm()
	if form.validate_on_submit():
		search_str = form.search_string.data
		# category_name = "mobiles" #laptops
		category_name = "laptops" #laptops
		return redirect(url_for('post.search',search_string=search_str, category_name=category_name))
	return render_template('home.html',form=form, title="Aftab's Shopping Website")

@main.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
    else:
        session['visits'] = 1 # setting session data
    return "Total visits: {}".format(session.get('visits'))

@main.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None) # delete visits
    return 'Visits deleted'

@main.route('/compare_cart/', methods=['GET'])
def compare_cart():
	# Display all the session data.
	all_item_ids = session.get('cart')
	if all_item_ids:
		items = Items.query.filter(Items.id.in_(tuple(all_item_ids))).all()
	# Display all the items
		print(items)
	return 'All items in compare cart'
