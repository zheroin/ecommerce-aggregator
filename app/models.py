import uuid
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


class User(Base, UserMixin):
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first = db.Column(db.String, nullable=False)
    last = db.Column(db.String, nullable=False)

    public_key = db.Column(db.String, unique=True, nullable=False)

    watch_list_items = db.relationship(
        'TrackedItems', backref='user', lazy='dynamic')

    @property
    def full_name(self):
        return f'{self.first} {self.last}'.capitalize()

    def __init__(self, email, hashed_password, first, last, *args, **kwargs):
        self.password = hashed_password
        self.email = email
        self.first = first
        self.last = last
        self.public_key = uuid.uuid4().hex
        super().__init__(*args, **kwargs)

    def get_user_token(self, expiry_seconds=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiry_seconds)
        return s.dumps({'public_key': self.public_key}).decode('utf-8')

    @staticmethod
    def verify_user_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            public_key = s.loads(token).get('public_key')
        except:
            return None
        return User.query.filter_by(public_key=public_key).first()

    def __repr__(self):
        return f"<{self.first}> - <{self.email}>"


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
                        db.Column('item_id', db.Integer, db.ForeignKey(
                            'items.id'), primary_key=True),
                        db.Column('result_id', db.Integer, db.ForeignKey(
                            'results.id'), primary_key=True)
                        )

# Categories available:
# laptops, mobiles
# fashion


class Results(Base):
    search_string = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    items = db.relationship('Items', secondary=item_results,
                            lazy='subquery', backref=db.backref('results', lazy=True))

    def __repr__(self):
        return f'ID - {self.id} - Search - {self.search_string}'


class Items(Base):
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'))
    item_uuid = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String, nullable=False)
    item_name = db.Column(db.String, nullable=False)
    item_url = db.Column(db.String, unique=True, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    item_image = db.Column(db.String)
    item_details = db.Column(db.String)

    tracked = db.relationship(
        'TrackedItems', backref='search_item', lazy='dynamic')

    def __init__(self, retailer_id, category, item_name, item_url, item_price, item_image=None, item_details=None, *args, **kwargs):
        self.retailer_id = retailer_id
        self.category = category
        self.item_image = item_image
        self.item_name = item_name
        self.item_url = item_url
        self.item_price = item_price
        self.item_uuid = uuid.uuid4().hex
        self.item_details = item_details

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'Item {self.item_name} - url - {self.item_url}'


class TrackedItems(Base):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    search_item_id = db.Column(
        db.Integer, db.ForeignKey('items.id'), nullable=False)
    item_uuid = db.Column(db.String, unique=True, nullable=False)
    item_url = db.Column(db.String, nullable=False)
    item_name = db.Column(db.String, nullable=False)
    item_image = db.Column(db.String)
    current_price = db.Column(db.Integer, nullable=False)
    desired_price = db.Column(db.Integer)
    notification_sent = db.Column(db.Boolean, default=False)
    notification_date = db.Column(db.DateTime)
    last_extracted_timestamp = db.Column(
        db.DateTime, default=db.func.current_timestamp())

    def __init__(self,
                 user_id,
                 search_item_id,
				 item_name,
				 item_url,
				 current_price,
				 desired_price,
				 item_image=None,
				 notification_sent=None,
				 notification_date=None,
				 *args, **kwargs):
        self.user_id = user_id
        self.search_item_id = search_item_id
        self.item_image = item_image
        self.item_name = item_name
        self.item_url = item_url
        self.current_price = current_price
        self.desired_price = desired_price
        self.item_uuid = uuid.uuid4().hex
        self.notification_sent = notification_sent
        self.notification_date = notification_date

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<URL {self.item_url} - Name - {self.item_name} - Current Price {self.current_price} - Last extracted data {self.last_extracted_timestamp}>"
