import os
# os.system('start mongod')
from flask_pymongo import pymongo ,MongoClient

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = 'App'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    APP_MAIL_SUBJECT_PREFIX = '[App]'
    APP_MAIL_SENDER = 'App Admin <moneywangu@gmail.com>'
    APP_ADMIN = os.environ.get('APP_ADMIN')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    APP_ESTATES_PER_PAGE=20
    APP_LATEST_ESTATES_PER_PAGE=4
    APP_POSTS_PER_PAGE = 20
    APP_USERS_PER_PAGE=20
    APP_COMMENTS_PER_PAGE = 20
    APP_SLOW_DB_QUERY_TIME = 0.5
    # Uploads
    UPLOADS_DEFAULT_DEST ='D:/KING Downloads/Software Projects/twreapp/app/static/img/uploads/'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img/uploads/'
    UPLOADED_IMAGES_DEST = 'D:/KING Downloads/Software Projects/twreapp/app/static/img/uploads/'
    UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/uploads/'
    # MONGO_URI ='mongodb://localhost:27017/twredb'
    
    # MONGO_URI = "mongodb+srv://twredb:<youla2019twre%24>@cluster0-igeuf.mongodb.net/test?retryWrites=true&w=majority"
    # MONGO_DBNAME ='twredb'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    

class TestingConfig(Config):
    TESTING = True
    
class ProductionConfig(Config):
    DEBUG = False



config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}