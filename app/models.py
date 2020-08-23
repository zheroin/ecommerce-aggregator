from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True,nullable=False)
	password = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(120), unique=True,nullable=False)
	first = db.Column(db.String(30), nullable = False)
	last = db.Column(db.String(30), nullable = False)

	watch_list_items = db.relationship('Watchlist', backref='user', lazy='dynamic')

	def to_dict(self):
		data = {
			'id' : self.id,
			'username' : self.username,
			'email' : self.email,
			'first' : self.first,
			'last' : self.last
		}

		return data

	def get_reset_token(self, expiry_seconds = 1800):
		s = Serializer(current_app.config['SECRET_KEY'], expiry_seconds)
		return s.dumps({'user_id' : self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token).get('user_id')
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"<{self.username}> - <{self.email}>"

class Results(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	search_string = db.Column(db.String(30), nullable=False)
	retailer_name = db.Column(db.String(30), nullable=False) # Should point to retailers table eventually
	last_update_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
	all_items = db.relationship('Items', backref = 'results', lazy = 'dynamic')

	def __repr__(self):
		return f'Results for {self.search_string} and retailer {self.retailer_name}'

class Items(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	search_id = db.Column(db.Integer, db.ForeignKey('results.id'))
	item_name = db.Column(db.String(150), nullable = False)
	item_url = db.Column(db.String(150), nullable= False)
	item_price = db.Column(db.Integer, nullable= False)
	item_image = db.Column(db.String(150))

	watchlist_rec = db.relationship('Watchlist', backref='item', lazy='dynamic')

	def __repr__(self):
		return f'Item {self.item_name} - url - {self.item_url}'

class Watchlist(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable= False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
	desired_price = db.Column(db.Integer, nullable = False)

	def __repr__(self):
		return f'Item ID - {self.item_id}, User ID {self.user_id}'

class Retailer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True, nullable=False)
	home_url = db.Column(db.String(30), unique=True, nullable=False)
	search_url = db.Column(db.String(30), unique=True, nullable=False)
	sorting_details = db.Column(db.Text) # Contains a JSON string of ==> Python Dict of sorting options for each Retailer

	# Sorting Columns : 
	# price_high_to_low = db.Column(db.String(30))
	# price_low_to_high = db.Column(db.String(30))
	# cust_reviews = db.Column(db.String(30))
	# newest_arrivals = db.Column(db.String(30))
	# featured = db.Column(db.String(30))
	# Sorting columns end

	def __repr__(self):
		return f"Retailer <{self.name}>"


