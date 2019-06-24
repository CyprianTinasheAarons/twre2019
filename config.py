import os
import cloudinary 

basedir = os.path.abspath(os.path.dirname(__file__))

cloudinary.config(
    cloud_name="twre",
    api_key="299545698238123",
    api_secret="wVP91fLanBoeP3twmRxJvcAZer0"
)

class Config:
    APP_NAME = 'App'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    APP_ESTATES_PER_PAGE=20
    APP_LATEST_ESTATES_PER_PAGE=4
    APP_POSTS_PER_PAGE = 20
    APP_USERS_PER_PAGE=20
    APP_COMMENTS_PER_PAGE = 20
    APP_SLOW_DB_QUERY_TIME = 0.5
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
   
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