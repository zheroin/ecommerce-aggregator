from run import app
from app.models import User, Retailer, Categories, Results, Items, TrackedItems, Watchlist
from app import db

with app.app_context():
    ## Add shops to the database
    # Adding Amazon
    ret = Retailer.query.filter(Retailer.name == 'amazon').first()
    print(ret.id)
    ## Add categories:
    ### Laptops - Amazon -
