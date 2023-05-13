import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import env_object 

app = Flask(__name__)

app.config.from_object(env_object)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views
from app import models

with app.app_context():
    db.create_all()