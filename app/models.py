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

	watch_list_items = db.relationship('TrackedItems', backref='user', lazy='dynamic')

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

	items = db.relationship('Items', backref="retailer", lazy="dynamic")

	@classmethod
	def get_retailer_ids(cls):
		return dict(cls.query.with_entities(cls.name, cls.id).all())

	def __repr__(self):
		return f"Retailer <{self.name}>"

item_results = db.Table('item_results',
db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
db.Column('result_id', db.Integer, db.ForeignKey('results.id'), primary_key=True)
)

# Categories available:
# laptops, mobiles
# fashion

class Results(Base):
	search_string = db.Column(db.String, nullable=False)
	category = db.Column(db.String)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	items = db.relationship('Items', secondary=item_results, lazy='subquery', backref=db.backref('results', lazy=True))

	def __repr__(self):
		return f'ID - {self.id} - Search - {self.search_string}'

class Items(Base):
	retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'))
	category = db.Column(db.String)
	item_name = db.Column(db.String, nullable = False)
	item_url = db.Column(db.String, unique=True, nullable= False)
	item_price = db.Column(db.Integer, nullable= False)
	item_image = db.Column(db.String)
	search_string1 = db.Column(db.String)
	search_string2 = db.Column(db.String)
	search_string3 = db.Column(db.String)
	search_string4 = db.Column(db.String)
	search_string5 = db.Column(db.String)
	tracked = db.relationship('TrackedItems', backref='search_item', lazy='dynamic')

	def __repr__(self):
		return f'Item {self.item_name} - url - {self.item_url}'

class TrackedItems(Base):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
	search_item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable= False)
	item_url = db.Column(db.String, nullable = False)
	item_name = db.Column(db.String, nullable = False)
	current_price = db.Column(db.Integer, nullable= False)
	desired_price = db.Column(db.Integer)
	notification_sent = db.Column(db.Boolean, default= False)
	notification_date = db.Column(db.DateTime)
	last_extracted_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	def __repr__(self):
		return f"<URL {self.item_url} - Name - {self.item_name} - Current Price {self.current_price} - Last extracted data {self.last_extracted_timestamp}>"




