from app import db
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, IntegerField, DateField, DateTimeField, DecimalField, PasswordField
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

class UserForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=3, max=50)])
    contact_number = TelField("Contact No.", validators=[InputRequired(), Length(min=7, max=11)])
    email = EmailField("Email", validators=[InputRequired(), Length(min=3, max=30)])
    role = StringField("Role", validators=[InputRequired(), Length(min=3, max=30)])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class OrderForm(FlaskForm):
    customer_id = IntegerField("Customer Id", validators=[InputRequired()])
    order_date = DateField("Order date")
    delivery_date = DateField("Delivery Date", validators=[InputRequired()])
    delivery_time = DateTimeField("Delivery Time")
    quantity = IntegerField("Order Quantity", validators=[InputRequired()])
    q_diesel = IntegerField("Diesel Quantity")
    q_87 = IntegerField("87 Quantity")
    q_90 = IntegerField("90 Quantity")
    q_ulsd = IntegerField("ULSD Quantity")
    price = DecimalField("Price",)
    status = StringField("Status") # Pending, Cancelled, Confirmed, Delivering, Delivered
    
class AddressForm(FlaskForm):
    address_line_1 = StringField("Address Line 1", validators=[InputRequired()])
    city = StringField("City")
    parish = StringField("Parish", validators=[InputRequired()])
    country = StringField("Country", validators=[InputRequired()])
    postal_code = StringField("Area Code")