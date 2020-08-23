from flask import render_template, Blueprint, flash, redirect, url_for
from app.posts.forms import SearchForm
from app import db

main = Blueprint('main',__name__)

@main.route('/',methods=['GET','POST'])
@main.route('/home.html',methods=['GET','POST'])
@main.route('/home',methods=['GET','POST'])
def home():
	form = SearchForm()
	if form.validate_on_submit():
		search_str = form.search_string.data
		return redirect(url_for('post.search',search_string=search_str))
	return render_template('home.html',form=form, title="Aftab's Shopping Website")
