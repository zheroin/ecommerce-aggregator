import secrets, os

class Config:
	SECRET_KEY = os.environ.get('FLASK_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
	JOBS = [
        {
            'id': 'job1',
            'func': 'app.tasks:check_prices',
            'args': (),
            'trigger': 'interval',
            'minutes': 1
        },
		{
            'id': 'job2',
            'func': 'app.tasks:update_price',
            'args': (),
            'trigger': 'interval',
            'minutes': 1
        }
    ]

