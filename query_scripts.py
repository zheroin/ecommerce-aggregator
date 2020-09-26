from run import app
from app.models import User, Retailer, Categories, Results, Items, TrackedItems, Watchlist
from app import db

with app.app_context():
    ## Add shops to the database
    # Adding Amazon
    print(Results.query.all())
    res = Results.query.filter_by(id=1).first()
    print(len(res.items))
    print([item.item_name for item in res.items])