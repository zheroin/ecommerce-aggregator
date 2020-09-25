from run import app
from app.models import User, Retailer, Categories, Results, Items, TrackedItems, Watchlist
from app import db

with app.app_context():
    db.create_all()

    ## Add shops to the database
    # Adding Amazon
    amazon = Retailer(name="amazon", home_url='https://www.amazon.in/')
    db.session.add(amazon)
    flipkart = Retailer(name="flipkart", home_url='https://www.flipkart.com/')
    db.session.add(flipkart)
    db.session.commit()
    ## Add categories:
    ### Laptops - Amazon -
