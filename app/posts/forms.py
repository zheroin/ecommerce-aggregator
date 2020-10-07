from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField, SelectField
from wtforms.validators import DataRequired, Email, Length

class SearchForm(FlaskForm):
	search_string = StringField("Search",validators=[DataRequired()])
	category_name = SelectField("Category", validators=[DataRequired()],
	choices=[
		('mobiles','Mobile Phones'),
		('laptops','Laptops/ Computers'),
		('mensfashion',"Men's Fashion"),
		('womensfashion',"Women's Fashion")
		])

class WatchListForm(FlaskForm):
	desired_price =  StringField("Desired Value",validators=[DataRequired()])
	add_to_watch_list = SubmitField("Add Item to Watch List")

class DummyForm(FlaskForm):
	textfield = TextField(" Text field label")