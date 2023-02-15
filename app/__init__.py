from flask import Flask, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import env_object 
import os

app = Flask(__name__)

app.config.from_object(env_object)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models
