from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
	email = StringField("Email Address",validators=[DataRequired(),Email()])
	password = PasswordField("Password",validators=[DataRequired(),Length(8,16)])
	submit = SubmitField("Sign In")
	remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
	email = StringField("Email Address",validators=[DataRequired(),Email()])
	first = StringField("First Name",validators=[DataRequired()])
	last = StringField("Last Name",validators=[DataRequired()])
	password = PasswordField("Password",validators=[DataRequired(),Length(8,16)])
	confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField("Register")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError("This email is already taken. Please use another one.")

class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first = StringField("First Name")
    last = StringField("Last Name")
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
	email = StringField("Email Address",validators=[DataRequired(),Email()])
	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if not user:
			raise ValidationError("This email is not registered.")

class PasswordResetForm(FlaskForm):
	password = PasswordField("Password",validators=[DataRequired(),Length(8,16)])
	confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField("Reset Password")
