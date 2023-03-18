from app import app
from flask import Flask, url_for, redirect, flash, render_template, request, session
from app.controller.Address import Address
from app.controller.Admin import Admin
from app.controller.Customer import Customer
from app.controller.Driver import Driver
from app.controller.Order import Order
from app.controller.Report import Report
from app.controller.Reservation import Reservation
from app.controller.Schedule import Schedule
from app.controller.Truck import Truck
from app.controller.User import User

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404