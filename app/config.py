import os
from dotenv import load_dotenv
from flask import url_for


load_dotenv()

class Config(object):
    ENVIRONMENT="TEST"
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    TESTING = False
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './static/uploads') 
    RESOURCE_FOLDER = os.environ.get('RESOURCE_FOLDER', './static/resources') 
    
    DB_URI_STRING="mysql://{un}:{pw}@{host}/{db}"
    # Database credentials
    USERNAME="root"
    PASSWORD="iUZn3J31zO/w{{9n_9/NEQW!n"
    DATABASE="FESCO-TEST"
    HOST="localhost:3306" # other_host_options, i.e "localhost:3306", "127.0.0.1:3306", "192.168.100.90"
    
    SQLALCHEMY_DATABASE_URI = DB_URI_STRING.format(un=USERNAME,pw=PASSWORD,host=HOST,db=DATABASE) or 'sqlite:///' + os.path.join(BASEDIR, 'FESCO-TEST.db')
    
    def __repr__(self):
        return self.ENVIRONMENT
    
    
class ProductionConfig(Config):
    ENVIRONMENT="PRODUCTION"
    DATABASE="FESCO-001"
    
    SQLALCHEMY_DATABASE_URI = Config.DB_URI_STRING.format(un=Config.USERNAME,pw=Config.PASSWORD,host=Config.HOST,db=DATABASE) 
    

class DevelopmentConfig(Config):
    ENVIRONMENT="DEVELOP"
    DATABASE="FESCO-DEVELOP"
    
    SQLALCHEMY_DATABASE_URI = Config.DB_URI_STRING.format(un=Config.USERNAME,pw=Config.PASSWORD,host=Config.HOST,db=DATABASE)
    

class TestingConfig(Config):
    TESTING = True
    
    
ENV = {
    'default': Config(),
    'production': ProductionConfig(),
    'development': DevelopmentConfig(),
    'testing': TestingConfig()
}

env = ""
if os.environ.get("ENV") is not None: os.environ['ENV'] = env = os.environ.get("ENV").lower() # env values i.e.  "production", "development", "testing" 

if env not in ENV.keys() or env == "": 
    os.environ['ENV'] = env = "testing"
if env == "production": os.environ['FLASK_DEBUG'] = "False"
# print("ENV:", env)

env_object = ENV[env]

os.environ['USERNAME']=env_object.USERNAME
os.environ['PASSWORD']=env_object.PASSWORD
os.environ['DATABASE']=env_object.DATABASE
os.environ['HOST']=env_object.HOST
os.environ['ENVIRONMENT']=env_object.ENVIRONMENT
    
print("{0}ENVIRONMENT: {1}".format(" * ", env_object.__repr__()))