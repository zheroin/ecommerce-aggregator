from run import app
from app.models import User, Retailer,  Results, Items, TrackedItems
from app import db

with app.app_context():
    db.create_all()
    ###### db.drop_all()

    ## Add shops to the database
    # Adding Amazon
    amazon = Retailer(name="amazon", home_url='https://www.amazon.in/')
    db.session.add(amazon)
    # Adding flipkart
    flipkart = Retailer(name="flipkart", home_url='https://www.flipkart.com/')
    db.session.add(flipkart)
    # Adding croma
    croma = Retailer(name="croma", home_url="https://www.croma.com")
    db.session.add(croma)
    ## Adding ebay
    ebay = Retailer(name="ebay", home_url="https://in.ebay.com/")
    db.session.add(ebay)
    ## Adding myntra
    myntra = Retailer(name="myntra", home_url="https://www.myntra.com")
    db.session.add(myntra)
    ## Adding snap deal
    snapdeal = Retailer(name="snapdeal", home_url="https://www.snapdeal.com/")
    db.session.add(snapdeal)
    ## Adding bewakoof
    bewakoof = Retailer(name="bewakoof", home_url="https://www.bewakoof.com/")
    db.session.add(bewakoof)
    ## Adding shein
    shein = Retailer(name="shein",home_url = "https://www.shein.in/")
    db.session.add(shein)
    # Adding paytm
    paytm = Retailer(name="paytm", home_url="https://www.paytmmall.com/")
    db.session.add(paytm)
    db.session.commit()
