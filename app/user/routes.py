from flask import render_template, Blueprint, redirect, url_for, flash, request, session, current_app
from app.models import User, Watchlist, Items
from app import db, bcrypt, mail
from app.user.forms import RegisterForm, LoginForm, UpdateForm, RequestResetForm, PasswordResetForm
from app.user.utils import send_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_mail import Message
# from app.main.routes import home


user = Blueprint('user',__name__)

@user.route('/login.html', methods = ['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			if not next_page or url_parse(next_page).netloc != '':
				return redirect(url_for('main.home'))
			else:
				return redirect(next_page)
		flash('Email or password incorrect please try again')
		return redirect(url_for('user.login'))
	return render_template('login.html', form= form)

@user.route('/register.html', methods = ['POST','GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegisterForm()
	if request.method == "POST":
		print("request POST")
		if form.validate_on_submit():
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = User(email = form.email.data, first = form.first.data, last = form.last.data, username = form.username.data, password = hashed_password)
			db.session.add(user)
			db.session.commit()
			flash(f'User {form.username.data} has been registered!')
			return redirect(url_for('user.login'))
	return render_template('register.html', form= form)


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@user.route('/account', methods = ['POST','GET'])
@login_required
def account():
	form = UpdateForm()
	watchlist_items = current_user.watch_list_items.all()
	print(watchlist_items)
	item_ids = [x.item_id for x in watchlist_items]
	print(item_ids)
	items_list = Items.query.filter(Items.id.in_(item_ids))
	if form.validate_on_submit():
		current_user.first = form.first.data
		current_user.email = form.email.data
		current_user.username = form.username.data
		current_user.last = form.last.data
		flash('Your account has been updated!')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.first.data = current_user.first 
		form.last.data = current_user.last 
		form.email.data = current_user.email 
		form.username.data = current_user.username 
	return render_template('account.html',title = f'{current_user.username} Account', form = form, item_list = items_list, current_user = current_user)


@user.route('/reset_password', methods = ['POST','GET'])
def request_reset():
	if current_user.is_authenticated:
		flash('Please logout to reset password')
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		send_reset_email(user)
		flash('Reset details have been sent over email. Please check to reset.')
		return redirect(url_for('user.login'))
	return render_template('request_reset.html', form = form)


@user.route('/reset_password/<token>', methods = ['POST','GET'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if not user:
		flash('Invalid or Expired token')
		return redirect(url_for('user.request_reset'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('your password has been updated.')
		return redirect(url_for('user.login'))
	return render_template('reset-token.html', form = form)

	# if form.validate_on_submit():
