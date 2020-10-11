from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_apscheduler import APScheduler


db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
mail = Mail()
moment = Moment()
scheduler = APScheduler()

def create_app(config_class = Config):
	app = Flask(__name__)
	app.config.from_object(config_class)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	scheduler.init_app(app)
	scheduler.start()
	bcrypt.init_app(app)
	login.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	from app.main.routes import main
	from app.posts.routes import post
	from app.user.routes import user
	from app.errors.handlers import errors
	app.register_blueprint(main)
	app.register_blueprint(post)
	app.register_blueprint(user)
	app.register_blueprint(errors)
	login.login_view = 'user.login'
	return app