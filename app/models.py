from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(Base,UserMixin):
	username = db.Column(db.String, unique=True,nullable=False)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, unique=True,nullable=False)
	first = db.Column(db.String, nullable = False)
	last = db.Column(db.String, nullable = False)

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

	def get_user_token(self, expiry_seconds = 1800):
		s = Serializer(current_app.config['SECRET_KEY'], expiry_seconds)
		return s.dumps({'user_id' : self.id}).decode('utf-8')

	@staticmethod
	def verify_user_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token).get('user_id')
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"<{self.username}> - <{self.email}>"

class Retailer(Base):
	name = db.Column(db.String, unique=True, nullable=False)
	home_url = db.Column(db.String, unique=True, nullable=False)

	def __repr__(self):
		return f"Retailer <{self.name}>"

class Categories(Base):
	name = db.Column(db.String, unique=True, nullable=False)

	def __repr__(self):
		return f"Category name {self.name}"

shop_category = db.Table('shop_category',
db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
db.Column('retailer_id', db.Integer, db.ForeignKey('retailer.id'), primary_key=True),
db.Column('cat_url_key', db.String, nullable=False)
)

class Results(Base):
	search_string = db.Column(db.String, nullable=False)
	all_items = db.relationship('Items', backref = 'results', lazy = 'dynamic')

	def __repr__(self):
		return f'Results for {self.search_string} and retailer {self.retailer_name}'

class Items(Base):
	search_id = db.Column(db.Integer, db.ForeignKey('results.id'))
	retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'))
	item_name = db.Column(db.String, nullable = False)
	item_url = db.Column(db.String, nullable= False)
	item_price = db.Column(db.Integer, nullable= False)
	item_image = db.Column(db.String)

	def __repr__(self):
		return f'Item {self.item_name} - url - {self.item_url}'

watchlist_items = db.Table('watchlist_items',
db.Column('item_id',db.Integer, db.ForeignKey('tracked_items.id'), primary_key=True),
db.Column('watchlist_id', db.Integer, db.ForeignKey('watchlist.id'), primary_key=True)
)

class TrackedItems(Base):
	item_url = db.Column(db.String, nullable= False)
	current_price = db.Column(db.Integer, nullable= False)
	last_scraped_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	def __repr__(self):
		return f"URL {self.item_url} - Current Price {self.current_price} - Last extracted data {self.last_scraped_date}"


class Watchlist(Base):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
	desired_price = db.Column(db.Integer, nullable = False)
	notification_sent = db.Column(db.Boolean, default= False)
	notification_date = db.Column(db.DateTime)

	items = db.relationship('TrackedItems', secondary=watchlist_items, lazy='subquery', backref = db.backref('watchlists', lazy=True))

	def __repr__(self):
		return f'Item ID - {self.item_id}, User ID {self.user}'





