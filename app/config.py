import os
from dotenv import load_dotenv
from flask import url_for


load_dotenv()

class Config(object):
    ENVIRONMENT="TEST"
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    TESTING = False
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads') 
    
    DB_URI_STRING="mysql://{un}:{pw}@{host}/{db}"
    USERNAME="root"
    PASSWORD=""
    DATABASE="FESCO-TEST"
    HOST="localhost:3306" # other_host_options, i.e "localhost:3306", "127.0.0.1:3306", "192.168.100.90"
    
    DATABASE_URL=DB_URI_STRING.format(un=USERNAME,pw=PASSWORD,host=HOST,db=DATABASE) or 'sqlite:///' + os.path.join(BASEDIR, 'mydatabase.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    
    def __repr__(self):
        return self.ENVIRONMENT
    
    
class ProductionConfig(Config):
    ENVIRONMENT="PRODUCTION"
    USERNAME="root"
    PASSWORD=""
    DATABASE="FESCO-001"
    HOST="12.0.0.1:3306" # other_host_options, i.e "localhost:3306", "127.0.0.1:3306", "192.168.100.90"
    
    DATABASE_URL=Config.DB_URI_STRING.format(un=USERNAME,pw=PASSWORD,host=HOST,db=DATABASE)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL 
    

class DevelopmentConfig(Config):
    ENVIRONMENT="DEVELOP"
    USERNAME="root"
    PASSWORD=""
    DATABASE="FESCO-DEVELOP"
    HOST=Config.HOST # other_host_options, i.e "localhost:3306", "127.0.0.1:3306", "192.168.100.90"
    
    DATABASE_URL=Config.DB_URI_STRING.format(un=USERNAME,pw=PASSWORD,host=HOST,db=DATABASE)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    

class TestingConfig(Config):
    TESTING = True
    
    
ENV = {
    'default': Config(),
    'production': ProductionConfig(),
    'development': DevelopmentConfig(),
    'testing': TestingConfig()
}

env = os.environ.get("ENV").lower() # env values i.e.  "production", "development", "testing" 

if env not in ENV.keys() or env == "": 
    env = "testing"
    os.environ['ENV'] = env
if env == "production": os.environ['FLASK_DEBUG'] = "False"

env_object = ENV[env]

os.environ['USERNAME']=env_object.USERNAME
os.environ['PASSWORD']=env_object.PASSWORD
os.environ['DATABASE']=env_object.DATABASE
os.environ['HOST']=env_object.HOST
os.environ['ENVIRONMENT']=env_object.ENVIRONMENT
    
print("{0} ENVIRONMENT: {1}".format(" *", env_object.__repr__()))