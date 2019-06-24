
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_pymongo import pymongo ,MongoClient
from config import config
from flask_login import LoginManager,UserMixin
from flask_caching import Cache
from .models import User
from flask_assets import Environment,Bundle


 
client = pymongo.MongoClient("mongodb+srv://twre:qwertyuiop@cluster0-igeuf.mongodb.net/test?retryWrites=true&w=majority")
mongo= client.twredb

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.Users
    user_json = users.find_one({'_id': 'Int32(user_id)' })
    return User(user_json)

assets = Environment()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
cache = Cache(config={'CACHE_TYPE': 'simple'})


js = Bundle('jquery.min.js', 'bootstrap.min.js', 'config.js','ekko-lightbox.min.js' , 'jquery.min.js' ,'list.min.js ','popper.min.js' ,'styles.js',filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config['default'])
    config['default'].init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    cache.init_app(app)
    assets.init_app(app)
    return app