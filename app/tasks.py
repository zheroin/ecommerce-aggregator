from flask import render_template
from flask_mail import Message
from app import scheduler,  mail, db
from app.models import TrackedItems, User, Items
from app.data.individual_price_scraper import IndividualScraper
import datetime, re

def clear_database():
	# print("Starting task.....")
	with scheduler.app.app_context():
		scheduler.app.logger.info("Starting task.........")
	# print("starting task......")
	# app = apscheduler.app
	# with app.app_context():
	# 	app.logger.info('Starting task')

def check_prices():
	app = scheduler.app
	app.logger.info("Starting check prices task.........")
	with app.app_context():
		all_items = TrackedItems.query.filter(TrackedItems.current_price > TrackedItems.desired_price,\
		TrackedItems.notification_sent != True).all()
		for item in all_items:
			user = item.user
			msg = Message('Password Reset Request',
					sender='pistaftab@gmail.com',
					recipients=[user.email])
			html_body = render_template('email/notification.html', user = user, item=item)
			msg.html = html_body
			app.logger.info(f"Sending email to {user.full_name} for item {item.item_name}")
			mail.send(msg)
			item.notification_sent = True
			item.notification_date = datetime.datetime.utcnow()
			app.logger.info(f"Notification status changed for item - {item.item_name}")
			db.session.commit()

def update_price():
	app = scheduler.app
	app.logger.info("Starting update prices task.........")
	with app.app_context():
		scraper = IndividualScraper()
		all_items = TrackedItems.query.filter(TrackedItems.notification_sent != True).all()
		try:
			for item in all_items:
				title, price = scraper.get_price(item.item_url)
				app.logger.info(f"Retrieved the curent price - {price} for {title}...")
				item.last_extracted_timestamp = datetime.datetime.utcnow()
				if price!= item.current_price:
					item.current_price = price
				db.session.commit()
		except Exception as e:
			app.logger.info(f"Error during scheduled task update_price - {e}")

