from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,SelectField,IntegerField,MultipleFileField 
from wtforms.validators import Required, Length ,Regexp,Email
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired 
from app import images
 

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me' ,validators=[Length(0, 100)])
    submit = SubmitField('Submit', id="btn")

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64),Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, ''numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', choices=[('admin','Admin'),('user','User')])
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit' ,id="btn" )

class PostForm(FlaskForm):
    title =StringField('Post Title', validators=[Required()])
    summary =TextAreaField('Post Summary', validators=[Required()])
    image = FileField('Post Image', validators=[FileAllowed(images, 'Images only!')])
    body =TextAreaField('Post Body', id="editor1", validators=[Required()])
    Submit1 = SubmitField('Post', id="btn")
    
class CommentForm(FlaskForm):
    body = StringField( validators=[Required()])
    submit = SubmitField('Submit' , id="btn")

class PropertyForm(FlaskForm):
    title =StringField('Property Title', validators=[Required()])
    category = SelectField('Category', choices=[('For Sale','For Sale'),('For Letting','For Letting')])
    address = StringField('Address', validators=[Length(0, 64)])
    price = IntegerField('Price', validators=[])
    body = TextAreaField('Description' , id="editor1")
    images = MultipleFileField('Add Images', validators=[ FileAllowed(images, 'Images only!')])
    submit1= SubmitField('Submit' , id="btn")

class SearchForm(FlaskForm):
    search = StringField()
    submit2= SubmitField('Search', id="btn")
   
