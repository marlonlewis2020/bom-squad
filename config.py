import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class Config(object):
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads') 
    # DB_URI_STRING = os.environ.get('DB_URI_STRING')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mydatabase.db')

    
    def __repr__(self):
        return "DEFAULT"
    
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'mydatabase.db'))
    
    def __repr__(self):
        return "PRODUCTION"
    

class DevelopmentConfig(Config):
    
    def __repr__(self):
        return "DEVELOPMENT"
    

class TestingConfig(Config):
    TESTING = True
    
    def __repr__(self):
        return "TESTING"
    
    
ENV = {
    'default': Config(),
    'production': ProductionConfig(),
    'development': DevelopmentConfig(),
    'testing': TestingConfig()
}