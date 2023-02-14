import os
from dotenv import load_dotenv


load_dotenv()

class Config(object):
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads') 
    DB_URI_STRING = os.environ.get('DB_URI_STRING')
    USERNAME=os.environ.get('USERNAME')
    PASSWORD=os.environ.get('PASSWORD')
    DATABASE=os.environ.get('DATABASE')
    HOST=os.environ.get('HOST')
    
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URL=DB_URI_STRING.format(un=USERNAME,pw=PASSWORD,host=HOST,db=DATABASE) or 'sqlite:///' + os.path.join(BASEDIR, 'mydatabase.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'mydatabase.db')
    
    def __repr__(self):
        return "DEFAULT"
    
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URL 
    
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