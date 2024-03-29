from app import db
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, IntegerField, DateField, DateTimeField, DecimalField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length

class CustomerForm(FlaskForm):
    address_id = IntegerField("Address Id", validators=[InputRequired()])
    company = StringField("Company", validators=[InputRequired(), Length(min=3, max=50)])
    branch = StringField("Branch", validators=[InputRequired(), Length(min=3, max=50)])
    officer = StringField("Purchasing Officer", validators=[InputRequired(), Length(min=3, max=30)])
    name = StringField("Name", validators=[InputRequired(), Length(min=3, max=50)])
    contact_number = TelField("Contact No.", validators=[InputRequired(), Length(min=7, max=11)])
    email = EmailField("Email", validators=[InputRequired(), Length(min=3, max=30)])
    role = StringField("Role", validators=[InputRequired(), Length(min=3, max=30)])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    location = StringField("Address Line 1", validators=[InputRequired(), Length(max=120)])
    
    address_line_1 = StringField("Address Line 1", validators=[InputRequired()])
    city = StringField("City")
    parish = StringField("Parish", validators=[InputRequired()])
    country = StringField("Country", validators=[InputRequired()])
    postal_code = StringField("Area Code")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=3, max=50)])
    contact_number = TelField("Contact No.", validators=[InputRequired(), Length(min=7, max=11)])
    email = EmailField("Email", validators=[InputRequired(), Length(min=3, max=30)])
    role = StringField("Role", validators=[InputRequired(), Length(min=3, max=30)])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    

class LoginForm (FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=80)])
    

class OrderForm(FlaskForm):
    customer_id = IntegerField("Customer Id", validators=[InputRequired()])
    delivery_date = StringField("Delivery Date", validators=[InputRequired()])
    delivery_time = StringField("Delivery Time")
    quantity = IntegerField("Order Quantity", validators=[InputRequired()])
    q_diesel = IntegerField("Diesel Quantity")
    q_87 = IntegerField("87 Quantity")
    q_90 = IntegerField("90 Quantity")
    q_ulsd = IntegerField("ULSD Quantity")
    price = DecimalField("Price")
    status = StringField("Status")
    location = IntegerField("Address Id", validators=[InputRequired()])
    preferred = StringField("Preferred Petrol")
    
class AddressForm(FlaskForm):
    address_line_1 = StringField("Address Line 1", validators=[InputRequired()])
    city = StringField("City")
    parish = StringField("Parish", validators=[InputRequired()])
    country = StringField("Country", validators=[InputRequired()])
    postal_code = StringField("Area Code")
    
class TruckForm(FlaskForm):    
    license_plate =  StringField("License Plate", validators=[InputRequired(), Length(max=20)])
    capacity = StringField("Capacity", validators=[InputRequired()])
    available = IntegerField("Available", validators=[InputRequired()])
    make = StringField("Make", validators=[InputRequired(), Length(max=50)])
    model = StringField("Model", validators=[InputRequired(), Length(max=50)])
    year = IntegerField("Capacity", validators=[InputRequired()])
    active = BooleanField("Active", validators=[InputRequired()])
    