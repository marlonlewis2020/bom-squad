from . import db
from datetime import datetime
from app.utils.utils import format_date, strtodate, sql_date
from flask_login import current_user
from itertools import permutations

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
        
    def repr(self):
        return {
            "name":self.name,
            "contact_number":self.contact_number,
            "email":self.email,
            "role":self.role,
            "username":self.username,
            "is_active":self.is_active
        }
        
    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        if current_user.id is not None:
            return True
        return False


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


class Driver(User):
    __tablename__ = 'driver'
    id = db.Column(db.Integer, db.ForeignKey(user_id), primary_key=True)
    license_number = db.Column(db.String(20), unique=True, nullable=False)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __init__(self, license_number, truck_id, status, user):
        super().__init__(user.name, user.contact_number, user.email, user.role, user.username, user.password)
        self.license_number = license_number
        self.truck_id = truck_id
        self.status = status
        print("Driver object created")

class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey(user_id), primary_key=True)
    group = db.Column(db.String(20), default="dispatcher")
    
    def __init__(self, group, user):
        super().__init__(user.name, user.contact_number, user.email, user.role, user.username, user.password)
        self.group = group


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
        self.delivery_date = (delivery_date, (strtodate(delivery_date)))[type(delivery_date)==str]
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

class Truck(db.Model):
    __tablename__="truck"
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=0)
    
    def __init__(self, license_plate, capacity, make, model, year, active=1):
        self.license_plate = license_plate
        cap = [int(x) for x in capacity.split(",")]
        total = sum(cap)
        self.capacity = total
        self.make = make
        self.model = model
        self.year = year
        self.active = active
        
    def permutations(self, q, lst):
        MAX = 0
        BEST = None

        for i in range(1,len(lst)+1):
            perm = list(permutations(lst, i))
            pris = [sum(x) for x in perm]
            for i, pri in enumerate(pris):
                if q>=pri and q> MAX:
                    MAX = pri
                    BEST = perm[i]
        return (MAX, BEST)
        
    def fill_each(self, order_id, qty, petrol, date, time, parish):
        
        # This is the priority Truck
        # Get the sizes of all its of its compartments
        comps = self.available_compartments()
        comp_cap_list = [x.capacity for x in comps]
        
        try:
            # get the available compartments of the existing delivery truck for later update
            delivery = db.session.query(Delivery).filter((Delivery.truck_id==comps[0].truck_id) & Delivery.available>0).first()
            if delivery is None:
                delivery = Delivery(order_id,petrol,date,time,self.id,parish,0,self.capacity)
                db.session.add(delivery)
                db.session.commit()
                db.session.refresh(delivery)
        except Exception as e:
            print(e)
        
        goal = min(qty, delivery.available)
        # call the permutation function
        perms_tuple = self.permutations(goal, comp_cap_list)
        
        amount = perms_tuple[0]
        if amount != 0:
            try:
                order = db.session.query(Order).filter_by(id=order_id).scalar()
                val, nest = perms_tuple
                
                if val:
                    for v in nest:    
                        comp = [x for x in comps if x.capacity==v][0]
                        
                        if delivery.available >= v:
                            # update delivery
                            delivery.available -= v
                            delivery.filled += v
                            
                            delivery_comp = DeliveryCompartment(delivery.id, order_id, comp.id, parish, petrol, comp.capacity)
                            db.session.add(delivery_comp)
                            match petrol:
                                # update the specific fuel type quantity
                                case "diesel":
                                    order.q_diesel += v
                                case "87":
                                    order.q_87 += v
                                case "90":
                                    order.q_90 += v
                                case "ulsd":
                                    order.q_ulsd += v
                
                # update the total order quantity
                order.quantity += val
                db.session.commit()
                qty -= val
            except IndexError as ie:
                print(ie)
                print(f"[x for x in comps if x.capacity==size][0]: comp is a {type(comp)}.")
            
            except Exception as e:
                created = False
                print(e)
                if created:
                    db.session.delete(delivery)
                    db.session.commit()
                    db.session.rollback()
        return qty
        
    def get_compartments(self):
        return [x for x in db.session.query(Compartment).filter_by(truck_id=self.id).all()]
    
    def available(self):
        delivery = db.session.query(Delivery).filter_by(truck_id=self.id).first()
        if not delivery:
            return self.capacity
        return self.capacity - delivery.available
    
    def available_compartments(self):
        # fc is filled or already booked compartments
        fc = db.session.query(DeliveryCompartment).join(Compartment, Compartment.id==DeliveryCompartment.compartment_id)\
        .join(Delivery, Delivery.truck_id==Compartment.truck_id).filter((Compartment.truck_id==self.id)).all()
        filled_compartments = [x.compartment_id for x in fc]
        available_comps = db.session.query(Compartment).filter((Compartment.truck_id==self.id) & (~Compartment.id.in_(tuple(filled_compartments)))).all()
        return available_comps
        
    def fill_all(self, order_id, qty, petrol, parish, date, time):
        created = False
        temp = 0
        if self.available() == self.capacity:
            try:
                order = db.session.query(Order).filter_by(id=order_id).scalar()
                # create a delivery
                delivery = Delivery(order_id, petrol, date, time, self.id, parish, 0, self.capacity)
                db.session.add(delivery)
                db.session.commit()
                created = True
                db.session.refresh(delivery)
                
                d_comps = self.get_compartments()
                for comp in d_comps:
                    if temp + comp.capacity <= qty:
                        # fill all compartments of this truck
                        temp += comp.capacity
                        comp = DeliveryCompartment( delivery.id, order_id, comp.id, parish, petrol, comp.capacity)
                        db.session.add(comp)
                match petrol:
                    # update the specific fuel type quantity
                    case "diesel":
                        order.q_diesel += temp
                    case "87":
                        order.q_87 += temp
                    case "90":
                        order.q_90 += temp
                    case "ulsd":
                        order.q_ulsd += temp
                # update the total order quantity
                order.quantity += temp
                delivery.filled += temp
                delivery.available -= temp
                db.session.commit()
            except Exception as e:
                created = False
                print(e)
                if created:
                    temp = 0
                    db.session.delete(delivery)
                    db.session.commit()
                    db.session.rollback()
        elif self.available() > 0:
            self.fill_each(order_id, self.available(), petrol, date, time, parish)
            
        return temp

        
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
    """ An order can be delivered by multiple trucks. 
        This is the dispatching of a specific truck, at a specific date/time.
        This sets the delivery assignment for a specific truck. 
        This delivery is tied to a specific date/time.
    """
    __tablename__="delivery"
    id = db.Column(db.Integer, primary_key=True) # specific to this truck on this date and time for this 1 full trip
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False) # specific truck
    date = db.Column(db.String(25), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    filled = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer)
    
    
    def __init__(self, order_id, petrol, date, time, truck_id, parish, qty):
        self.truck_id = truck_id
        self.date = date
        self.time = time
        self.filled = qty
        self.petrol = petrol
        self.order_id = order_id
        self.parish = parish
        self.available = db.session.query(Truck).filter_by(id=self.truck_id).first()
    
    def __init__(self, order_id, petrol, date, time, truck_id, parish, qty, available):
        self.truck_id = truck_id
        self.date = date
        self.time = time
        self.filled = qty
        self.petrol = petrol
        self.order_id = order_id
        self.parish = parish
        self.available = available
        
        
    def get_compartment_info(self):
        # use delivery id to get all filled compartments from DeliveryCompartment
        response = []
        result = db.session.query(DeliveryCompartment).join(Compartment, DeliveryCompartment.compartment_id==Compartment.id)\
        .add_columns(Compartment.order_id, DeliveryCompartment.compartment_no).filter(DeliveryCompartment.delivery_id==self.id).all()
        
        if result:
            response = [{
                "compartment_no":x[2],
                "order_no":x[1],
            } for x in result]
        return response
    
    def get_orders(self):
        """         
        gets all the orders or stops to make during this specific delivery trip.
        The orders/stops are determined by the filled compartments for this truck's delivery trip.
        This delivery is tied to a specific date/time.
        """        
        orders = []
        order_nos = [x[0] for x in db.session.query(DeliveryCompartment.order_no).distinct().filter_by(delivery_id=self.id).all()]
        for id in order_nos:
            try:
                customer = db.session.query(Address, Customer, User, Order)\
                    .filter(
                        (Address.id==Customer.address_id)\
                        & (Customer.id==User.id)\
                        & (User.id==Order.customer_id)\
                        & (Order.id==id)).first()
                
                address = "{0} {1}, {2}, {3}, {4}".format(customer.Address.address_line_1, customer.Address.city, customer.Address.parish, customer.Address.country, customer.Address.postal_code)
                orders.append( Order.to_json( customer.Order, customer.User.name, address ))           
            except Exception as e:
                print(e)     
        return orders
        
class DeliveryCompartment(db.Model):
    """ A single delivery for a truck can span multiple compartments for one or more orders. 
    Hence compartments must indicate petrol type and order number. 
    As delivery is for a specific trip (truck, date and time) - this is also an assignment of compartments for a specific trip.
    However, this assignment is one that forms a compartment/order set for a specific order on the specific trip. """
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False) # associated with a single truck
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False) # could be associated with multiple trucks
    compartment_id = db.Column(db.Integer, db.ForeignKey('compartment.id'), nullable=False)
    parish = db.Column(db.String(20), nullable=False) # this
    petrol = db.Column(db.String(6), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    def __init__(self, delivery_id, order_id, compartment_id, parish, petrol, qty):
        self.qty = qty
        # delivery = db.session.query(Delivery).filter_by(id=self.delivery_id).first()
        # comp = db.session.query(Compartment.capacity).filter_by(id=compartment_id).first()[0]
        self.delivery_id = delivery_id
        self.compartment_id = compartment_id
        self.parish = parish
        self.petrol = petrol
        # assign order id to this compartment
        self.order_id = order_id
        # update delivery available balance
        
            
    def __is_valid(self):
        comp = db.session.query(Compartment.capacity).filter_by(id=self.compartment_id).first()[0]
        return self.qty >= comp
    
    def save(self):
        if self.__is_valid():
            try:
                db.session.add(self)
                # update the delivery
                delivery = db.session.query(Delivery).filter_by(id=self.delivery_id).scalar()
                delivery.filled += self.qty
                delivery.available -= self.qty
                db.session.commit()
                return True
            except Exception as e:
                print(e)
        return False
            
        
class Compartment(db.Model):
    __tablename__="compartment"
    id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    compartment_no = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    
    def __init__(self, truck_id, compartment_no, capacity):
        self.truck_id = truck_id
        self.compartment_no = compartment_no
        self.capacity = capacity
        
class Area(db.Model):
    __tablename__="area"
    area = db.Column(db.String(20), primary_key=True)
    neighbour = db.Column(db.String(20), primary_key=True)
    
    def __init__(self, area_id, nbr_id):
        self.area = area_id
        self.neighbour = nbr_id