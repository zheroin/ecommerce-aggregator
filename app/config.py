import secrets, os

class Config:
	SECRET_KEY = os.environ.get('FLASK_KEY') or '2f31393c624a76c7c0266affdbcfdf25' 
	SQLALCHEMY_DATABASE_URI = 'sqlite:///test1.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

