import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import env_object 

app = Flask(__name__)

app.config.from_object(env_object)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

LOCKED = {}
PEND = {}

from app import views
from app import models



with app.app_context():
    db.create_all()
    
    # insert areas
    areas_loaded = db.session.query(models.Area).count()
    if not areas_loaded:
        with open("Areas.csv","r") as areas:
            rows = [area.split(",") for area in areas]
            
        for nbrs in rows:
            print(nbrs[0], nbrs[1])
            area = models.Area(nbrs[0], nbrs[1])
        print(len(rows))
        db.session.add(area)
        db.session.commit()
    
