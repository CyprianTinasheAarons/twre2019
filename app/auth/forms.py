from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length , Regexp , EqualTo
from wtforms import ValidationError


class LoginForm(Form):
    email = StringField('Email', validators=[Required(),Length(1,64),Email()])
    password =PasswordField('Password' ,validators=[Required()])
    remember_me =BooleanField('keep me logged in')
    submit = SubmitField('Login', id='btn')
 
class SignupForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, ''numbers, dots or underscores')])
    password = PasswordField('Password' , validators=[ Required(), Length(8, 15), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('SignUp', id='btn')


   