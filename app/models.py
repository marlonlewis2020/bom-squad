from . import db
from datetime import datetime
from app.utils.utils import format_date, strtodate
from flask_login import current_user

user_id = 'user.id'

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __init__(self, name, contact_number, email, role, username, password):
        self.name = name
        self.contact_number = contact_number
        self.email = email
        self.role = role
        self.username = username
        self.password = password
        self.is_active = True
        print("User object created")
        
    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        if current_user.id is not None:
            return True
        return False

    # __mapper_args__ = {
    #     'polymorphic_identity': 'user',
    #     'polymorphic_on': role
    # }

class Customer(User):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    officer = db.Column(db.String(30), nullable=False)
    
    def __init__(self, address_id, company, branch, officer, user):
        super().__init__(user.name, user.contact_number, user.email, user.role, user.username, user.password)
        self.id = user.id
        self.address_id = address_id
        self.company = company
        self.branch = branch
        self.officer = officer
        print("Customer object created")

    # __mapper_args__ = {
    #     'polymorphic_identity': 'customer',
    # }

class Driver(User):
    __tablename__ = 'driver'
    id = db.Column(db.Integer, db.ForeignKey(user_id), primary_key=True)
    license_number = db.Column(db.String(20), unique=True, nullable=False)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'driver',
    # }

class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey(user_id), primary_key=True)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'admin',
    # }

class Order(db.Model):
    __tablename__="order"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_date = db.Column(db.Date, nullable=False)
    delivery_time = db.Column(db.String(20))
    quantity = db.Column(db.Integer, nullable=False)
    q_diesel = db.Column(db.Integer)
    q_87 = db.Column(db.Integer)
    q_90 = db.Column(db.Integer)
    q_ulsd = db.Column(db.Integer)
    price = db.Column(db.Numeric(10,2), default=0.00)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Pending") # Pending, Cancelled, Preparing, Ready, Delivering, Delivered
    
    def __init__(self, id, customer_id, delivery_date, delivery_time, quantity, q_diesel, q_87, q_90, q_ulsd, price, status):
        if id is not None: self.id = id
        self.customer_id = customer_id
        self.order_date = datetime.utcnow()
        self.delivery_date = (delivery_date, strtodate(delivery_date))[type(delivery_date)==str]
        self.delivery_time = delivery_time
        self.quantity = quantity
        self.q_diesel = q_diesel
        self.q_87 = q_87
        self.q_90 = q_90
        self.q_ulsd = q_ulsd
        self.price = price
        self.status = status
    
    def to_json(self, customer_name:str, customer_address:str):
        """Converts to a dictionary reponse

        Args:
            customer_name (str): name of customer
            customer_address (str): customer's address
            delivery_time (str): time for the delivery

        Returns:
            json object: Json repsonse to send to front end
        """
        return {
            "orderID":self.id,
            "orderQuantity":self.quantity,
            "q_diesel": self.q_diesel,
            "q_87": self.q_87,
            "q_90": self.q_90,
            "q_ulsd": self.q_ulsd,
            "customerName":customer_name,
            "address":customer_address,
            "deliveryDate":self.delivery_date,
            "deliveryTime":self.delivery_time,
            "status":self.status
        }    

class Address(db.Model):
    __tablename__="address"
    id = db.Column(db.Integer, primary_key=True)
    address_line_1 = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), default="")
    parish = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(30), default="Jamaica", nullable=False)
    postal_code = db.Column(db.String(10), default="JMAKN03", nullable=False)
    
    def __init__(self, address_line_1, city, parish, country="Jamaica", postal_code="JMAKN03"):
        self.address_line_1 = address_line_1
        self.city = city
        self.parish = parish
        self.country = country
        self.postal_code = postal_code
        print("Address object created")
    
    def __init__(self, address_line_1, city, parish, country="Jamaica"):
        self.address_line_1 = address_line_1
        self.city = city
        self.parish = parish
        self.country = country
        self.postal_code = "JMAKN03"
        print("Address object created")

class Truck(db.Model):
    __tablename__="truck"
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=0)
    
    def __init__(self, license_plate, capacity, make, model, year, active=1):
        self.license_plate = license_plate
        cap = [int(x) for x in capacity.split(",")]
        total = sum(cap)
        self.capacity = total
        self.available = total
        self.make = make
        self.model = model
        self.year = year
        self.active = active
        
    def repr(self):
        return {
            "id":self.id,
            "license_plate":self.license_plate,
            "capacity":self.capacity,
            "available":self.available,
            "make":self.make,
            "model":self.model,
            "year":self.year,
            "active":self.active
        }

class Delivery(db.Model):
    __tablename__="delivery"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    parish = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(25), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    
    def __init__(self, order_id, truck_id, address_id):
        self.order_id = order_id
        self.truck_id = truck_id
        self.address_id = address_id
        address = db.session.query(Address).filter_by(id=address_id).first()
        self.parish = address.parish
        order = db.session.query(Order).filter_by(id=order_id).first()
        self.date = format_date(order.delivery_date)
        self.time = order.delivery_time
        
class Compartments(db.Model):
    __tablename__="compartments"
    id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    order_id = db.Column(db.Integer, default=0)
    compartment_no = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    petrol = db.Column(db.String(6), default="")
    
    def __init__(self, truck_id, compartment_no, capacity):
        self.truck_id = truck_id
        self.order_id = 0
        self.compartment_no = compartment_no
        self.capacity = capacity
        
class Area(db.Model):
    __tablename__="area"
    area = db.Column(db.String(20), primary_key=True)
    neighbour = db.Column(db.String(20), primary_key=True)
    
    def __init__(self, area_id, nbr_id):
        self.area = area_id
        self.neighbour = nbr_id