from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
class SignupForm(Form):
	first_name = StringField('First name', validators=[DataRequired("please enter your first name")])
	last_name = StringField('Last name', validators=[DataRequired("please enter your last name")])
	email = StringField('Email', validators=[DataRequired("please enter your email"), Email("your email is incorrect")])
	password = PasswordField('Password', validators=[DataRequired("please enter your password"), Length(min=6, message="The password must be 6 or more character")])
	submit = SubmitField('Sign up')
class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired("please Enter your email address"), Email("please Enter your email address")])
	password = StringField('password', validators=[DataRequired("please enter your email address")])
	submit = SubmitField("Sign in")