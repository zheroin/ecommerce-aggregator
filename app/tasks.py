from flask import current_app as app

def clear_database(app):
	# print("Starting task.....")
	with app.app_context():
		app.logger.info("Starting task.........")
	# app = apscheduler.app
	# with app.app_context():
	# 	app.logger.info('Starting task')