import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler
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
login.login_view = 'user.login'
mail = Mail()
moment = Moment()
scheduler = APScheduler()

def create_app(config_class = Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	scheduler.init_app(app)
	scheduler.start()
	bcrypt.init_app(app)
	login.init_app(app)
	mail.init_app(app)
	moment.init_app(app)

	from app.main.routes import main
	app.register_blueprint(main)

	from app.posts.routes import post
	app.register_blueprint(post)

	from app.user.routes import user
	app.register_blueprint(user)

	from app.errors.handlers import errors
	app.register_blueprint(errors)


	if app.config['LOG_TO_STDOUT']:
		stream_handler = logging.StreamHandler()
		stream_handler.setLevel(logging.INFO)
		app.logger.addHandler(stream_handler)
	else:
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/shopify.log', maxBytes=10240, backupCount=10)
		file_handler.setFormatter(logging.Formatter(
			'%(asctime)s %(levelname)s: %(message)s '
			'[in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info('Shopify startup')

	with app.app_context():
		db.create_all()

	return app