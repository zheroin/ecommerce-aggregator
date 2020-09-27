from app import scheduler
from app.models import TrackedItems, User

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
	with app.app_context():
		app.logger.info("Starting task.........")
		all_items = TrackedItems.query.all()
		print(all_items)
		# for item in all_items:
		# 	if item.current_price <= item.desired_price:
		# 		user = item.user.first
		# 		app.logger.info(f"Sending email to {user}")
		# 	else:
		# 		app.logger.info("No mail to be sent")
		# Send email.
