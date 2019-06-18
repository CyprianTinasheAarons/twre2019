from flask  import render_template
from . import auth
import bcrypt
from flask import render_template, redirect, request, url_for, flash,session ,g
from flask_login import login_user , logout_user, login_required ,login_manager, UserMixin
from flask_pymongo import pymongo ,MongoClient
from .forms import LoginForm
from .forms import SignupForm
from datetime import datetime
from ..email import send_email
from flask_login import current_user
from ..models import User
from app import cache


client = pymongo.MongoClient("mongodb+srv://twre:qwertyuiop@cluster0-igeuf.mongodb.net/test?retryWrites=true&w=majority")
mongo= client.twredb


# Should be hidden 
salt = b'$2b$07$Kw/qwGlHgmUwSgX4InYrMe'

def getNextSequence(collection,name):
     return collection.find_and_modify(query= { '_id': name },update= { '$inc': {'seq': 1}}, new=True ).get('seq')

@auth.route('/auth/login' , methods =['GET', 'POST'])
@cache.cached(timeout=300, key_prefix="login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = mongo.db.Users
        
        loginuser_json = users.find_one({'email' : request.form['email']})
        query= users.find({'email': request.form['email']},{'role':'1'})
        for i in query:
            dbRole = i['role']
        if loginuser_json:
            if bcrypt.hashpw((request.form['password']).encode('utf-8'), salt)  == loginuser_json['password']:
                loginuser = User(loginuser_json)
                login_user(loginuser, form.remember_me.data)
                session['email'] = request.form['email']
                flash('You have been login.')
                if  dbRole == 'admin':
                    return redirect(url_for('main.admin'))
                else:
                    return redirect(url_for('main.home'))
        flash('Invalid username or password?')

    return render_template('auth/login.html', form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear() 
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth.route('/auth/signup', methods=['GET', 'POST'])
@cache.cached(timeout=300, key_prefix="signup")
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        
        users  = mongo.db.Users
        existing_user = users.find_one({'username': request.form[ 'username'] })

        if existing_user is None:
            hashpass = bcrypt.hashpw((request.form['password']).encode('utf-8'), salt)
            users.insert({'_id': getNextSequence(mongo.db.Counters,"userId"),'username' : request.form['username'], 'email' : request.form['email'] ,'password': hashpass, 'name': '' , 'location': '', 'about_me': '' ,'role':'user', 'Date': datetime.now()})
        
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html' , form=form)

