from datetime import datetime
from MySQLdb import IntegrityError
from app import app, db
from flask import Flask, url_for, redirect, request, session, make_response
from .models import Customer, User, Address, Order, Delivery
from .forms import CustomerForm, AddressForm, OrderForm, UserForm
from werkzeug.security import generate_password_hash
# from app.utils import Address, Admin, Customer, Driver, Order, Report, Reservation, Schedule, Truck, User

IN_PROGRESS = {
    'status': 'error',
    'message': 'In progress!'
}

INVALID = {
    'status': 'error',
    'message': 'Invalid method!'
}

# # # -- End-Points -- # # #
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


# -- CUSTOMER END POINTS -- 

@app.route('/api/v1/customers/<id>', methods=['GET','PUT'])
def customer(id):
    # get customer or updates customer by id
    if request.method == 'GET':
        # GET THE ORDER DETAILS
        ''' VIEW RETURN EXAMPLE BELOW:
        {
            status: "success",
            data: {
                customerID: "00000001",
                company:"Total",
                branch:"Barbican",
                phoneNumbers:["(876)-555-0555","(876)-555-1555"],
                email:"totalbarbican@gmail.com",
                purchasingOfficer:"Robert Desnoes",
                location:"12 Barbican Road, Barbican, St. Andrew, Ja.",
            }
        }
        '''
        response = {
            'status':'error',
            'message':'Customer not found!'
        }
            
        customer = db.session.query(Customer, User)\
            .filter(
                (Customer.id==User.id)\
                & (Customer.id==id)\
            )\
            .scalar()
            # .add_column(Customer.id, Customer.company, Customer.branch, Customer.officer, User.contact_number, User.email, Address.address_line_1, Address.city, Address.parish, Address.country)\
        
        if customer is not None:  
            location = db.session.query(Address).filter_by(id=customer.address_id).scalar() 
            address = "{} {}, {}, {}, {}".format(location.address_line_1, location.city, location.parish, location.country, location.postal_code)
            response = {
                'data':{
                    'customerID':customer.id,
                    'company':customer.company,
                    'branch':customer.branch,
                    'phoneNumber':customer.contact_number,
                    'email':customer.email,
                    'purchasingOfficer':customer.officer,
                    'location':address
                    }
            }
            response['status'] = 'success',
        
        return make_response(response)
    elif request.method == 'PUT':
        # Update Customer details by customer id
        
        ''' VIEW RETURN EXAMPLE BELOW:
        '''
        return make_response(IN_PROGRESS)
    return make_response(INVALID)


@app.route('/api/v1/customers', methods=['POST'])
def customers():
    #adds all the deatils of a customer
    if request.method == 'POST':
        ''' VIEW EXAMPLE OF PASSED PARAMS BELOW:
            name:"John Doe",
            company:"Total",
            branch:"Barbican",
            username:"total_barbican",
            password:"password123",
            role:"customer",
            contact_number:"(876)-555-0555",
            email:"totalbarbican@gmail.com",
            officer:"Robert Desnoes",
            location:"12 Barbican Road, Barbican, St. Andrew, Ja."

        VIEW WXAMPLE OF RETURN VALUE BELOW:
        {
            status: "success"
        }
        '''
        response = {
                "status":"error",
                "message":"Something went wrong while adding "
            }
        form = CustomerForm()
        
        address = form.location.data.split(",")
        if len(address)==3:
            address = Address(address[0], address[1], address[2])
        elif len(address)==4:
            address = Address(address[0], address[1], address[2], address[3])
        elif len(address)==5:
            address = Address(address[0], address[1], address[2], address[3], address[4])
            
        user = User(form.name.data or "{} {}".format(form.company.data.trim(), form.branch.data.trim()), form.contact_number.data, form.email.data, form.role.data, form.username.data, generate_password_hash(form.password.data))
        address_added = False
        customer_added = False
        
        try:
            db.session.add(address)
            db.session.commit()
            address_added = True
            db.session.refresh(address)
            
            customer = Customer(address.id, form.company.data, form.branch.data, form.officer.data, user) 
            db.session.add(customer)
            db.session.commit()
            customer_added = True
            db.session.refresh(customer)
            
            response = {
                "status":"success"
            }
            
        except Exception:
            db.session.rollback()
            if address_added:
                db.session.delete(address)
            else:
                response['message']+= "Address data"
                
            if customer_added:
                db.session.delete(user)
                db.session.delete(customer)
            else:
                if not address_added: response['message']+= ", and "
                response['message']+= "User data [Username Already exists], and Customer data"
                
            db.session.commit() 
            response['message']+=". All changes have been rolled back."
               
        return make_response(response)
    return make_response(INVALID)
    

@app.route('/api/v1/customers/contact/<id>', methods=['GET','POST', 'PUT'])
def contacts(id):
    # method adds, updates, gets or marks a customer's contact as deleted
    ''' MORE DETAILS TO BE PASSED '''
    if request.method == 'GET':
        # GET CONTACT DETAILS task
        return make_response(IN_PROGRESS)
    elif request.method == 'POST':
        # ADD CONTACT DETAILS
        return make_response(IN_PROGRESS)
    elif request.method == 'PUT':
        # UPDATE CONTACT DETAILS 
        return make_response(IN_PROGRESS)
    return make_response(INVALID)


# -- ORDERS END POINTS -- 

@app.route('/api/v1/orders/<id>', methods=['GET', 'PUT'])
def order(id):
    response = IN_PROGRESS
    # gets or updates an order
    if request.method ==    'GET':
        # GET THE ORDER DETAILS
        ''' VEIW RETURN EXAMPLE BLEOW:
        {
            status: "success",
            data:
            {
                orderID:"E10014",
                orderQuantity:60,
                diesel: 0,
                87: 30,
                90: 30,
                ulsd: 0,
                customerName:"Total Barbican",
                address:"12 Barbican Road, Barbican, St. Andrew, Jamaica",
                deliveryDate:"2023-04-30",
                deliveryTime:"12:00 PM"
            }    
        }
        '''
        order = db.session.query(Order).filter_by(id=id).scalar()
        customer = db.session.query(Customer, Address, User)\
            .filter(
                (Address.user_id==Customer.id)\
                & (User.id==Customer.id)\
                & (Customer.id==order.customer_id)\
        ).scalar()
        
        address = "{0} {1} {2} {3}".format(customer.address_line_1, customer.city, customer.parish, customer.country)
        response = Order.to_json( order, customer.name, address )
        
    elif request.method == 'PUT':
        # UPDATE THE ORDER DETAILS
        ''' VIEW RETURN EXAMPLE BELOW
        {
            status: "success"
        }
        '''
        form = OrderForm()
        order=db.session.query(Order).filter_by(id=id).scalar()
        order.delivery_date = form.delivery_date.data
        order.last_updated = datetime.utcnow()
        order.delivery_time = form.delivery_time.data
        order.quantity = form.quantity.data
        order.q_diesel = form.q_diesel.data
        order.q_87 = form.q_87.data
        order.q_90 = form.q_90.data
        order.q_ulsd = form.q_ulsd.data
        order.price = form.price.data
        order.status = "Pending"
        db.session.add(order)
        db.session.commit()
        response = {
            "status": "success"
        }
    return make_response(response)
    
    
@app.route('/api/v1/orders', methods=['GET', 'POST'])
def orders(): 
    # gets all or adds an order
    response = {
        "status":"error"
    }
    if request.method == 'GET':
        # gets all orders
        ''' EXAMPLE OF RETURN VALUE 
        {
            status: "success",
            data:
            [ 
                {
                    orderID:"E10014",
                    orderQuantity:60,
                    diesel: 0,
                    87: 30,
                    90: 30,
                    ulsd: 0,
                    customerName:"Total Barbican",
                    address:"12 Barbican Road, Barbican, St. Andrew, Jamaica",
                    deliveryDate:<date:dateFormat>,
                    deliveryTime:<time:timeFormat>
                },
            ]   
        }
        '''
        response = {
            "status":"success",
            "data":[]
        }
        orders = db.session.query(Order)\
            .join(User, customer_id=User.id)\
            .join(Customer, customer_id=Customer.id)\
            .join(Address, Customer.address_id==Address.id)\
            .add_column(
                Order.id, Order.customer_id, Order.order_date, Order.delivery_date, 
                Order.delivery_time, Order.quantity, Order.q_diesel, Order.q_87,
                Order.q_90, Order.q_ulsd, Order.price, Order.last_updated, Order.status, 
                User.name, Address.address_line_1, Address.city, Address.parish, Address.country, Address.postal_code)\
            .all()
        for o in orders:
            response['data'].append(Order.to_json(o, ))
        pass
    elif request.method == 'POST':
        # adds an order
        ''' PARAMS EXAMPLE BELOW:
        "customer_id: 3
        q_diesel: 10,
        q_87: 50,
        q_90: 80,
        q_ulsd: 20,
        location: 5,
        quantity: 160,
        delivery_date: "June 3, 2023"
        delivery_time: "12:00 PM"
        '''
        ''' RETURN EXAMPLE BLEOW:
        {
            status: "pending",
            data: 
            {
                orderID:"E10016",
                requested:85,
                filled: 
                    {
                        volume: 80,
                        fuelBreakdown: [0,30,50,0],
                    }
                balance: 
                    {
                        volume: 5,
                        fuelBreakdown: [0,5,0,0],
                    }
                recommended:
                [
                    {
                        fuel:87, 
                        volume:[40],
                    },
                ]
            }
        }
        '''
        form = OrderForm()
        trucks = []
        
        # use best fit to fill the 
        
        order = Order(form.customer_id.data, form.delivery_date.data, form.delivery_time.data, form.quantity.data, form.q_diesel.data, form.q_87.data, form.q_90.data, form.q_ulsd.data, form.price.data, form.status.data)
        db.session.add(order)
        db.session.commit()
        db.session.refresh(order)
        
        for truck in trucks:
            delivery = Delivery(order.id, truck.id, form.location.data)
            db.session.add(delivery)
        db.session.commit()
        
        response = {
            "status": "success"
        }
    return make_response(response)

@app.route('/api/v1/orders/<id>', methods=['POST'])
def confirm_order(id, upgrade=False):
    """Confirm a pending order"""
    # if upgrade, assign the compartment for the truck in the global variable to this order id, and update the truck compartment's capacity
    # free up lock on table reords in global variable , and remove the order details from the global variable
    # i.e. locked_trucks_by_ids = {order_id:{'truck_id':1000,'compartment_ids':[2,3]}, order_id:{'truck_id':1001,'compartment_ids':[3]}
    # return status code 201 and success response
    pass

@app.route('/api/v1/orders/<id>', methods=['GET'])
def cancel_order(id):
    """Cancels the order"""
    # cancels an order by order id
    # check global to see if order is pending and if so, get the order details there
    # if order is not pending, lookup the order by the order id provided, remove the order details from the global variable
    # using the order details, find each truck in the order by the order id, mark the order as cancelled, empty the truck compartments that have been filled by that id 
    # free up lock on table reords in global variable 
    # i.e. locked_trucks_by_ids = {order_id:{'truck_id':1000,'compartment_ids':[2,3]}, order_id:{'truck_id':1001,'compartment_ids':[3]}
    # return status code 201 and success response
    return make_response(IN_PROGRESS)
    
    
@app.route('/api/v1/orders/schedule', methods=['GET'])
def get_schedule():
    # start=<date:dateForma/t>&end=<date:dateFormat>
    start = request.args.get('start')
    end = request.args.get('end')
    return make_response(IN_PROGRESS)
    
    
# -- TRUCK END POINTS --

@app.route('/api/v1/trucks', methods=['GET', 'POST'])
def trucks():
    if request.method == 'GET':
        # get a list of all trucks
        ''' VIEW RETURN EXAMPLE BELOW:
        {
            status: "success",
            data: 
            [
                {
                    truckNo:"TT807",
                    licenseNo:"2002LM",
                    orderComps:["E10015","E10015","E10014","E10014","E10015","E10015"],
                    sizeComps:[20,30,30,30,40,50],
                    contractor:"Paul Bogle"
                },
                {
                    truckNo:"TT805",
                    licenseNo:"2005LP",
                    orderComps:["E10016","E10016","E10016","","",""],
                    sizeComps:[20,30,30,30,40,50],
                    contractor:"Marcus Garvey"
                },
                {
                    truckNo:"JM2023",
                    licenseNo:"2007LR",
                    orderComps:["","","","","",""],
                    sizeComps:[20,30,30,30,40,50],
                    contractor:""Norman Manley""
                },
                {
                    truckNo:"CJ9647",
                    licenseNo:"2006LQ",
                    orderComps:["","","","","",""],
                    sizeComps:[20,30,30,30,40,50],
                    contractor:""Alex Bustamante""
                },
                {
                    truckNo:"TT008B",
                    licenseNo:"2003LN",
                    orderComps:["","","","","",""],
                    sizeComps:[20,30,30,30,40,50],
                    contractor:""Nanny Maroon""
                }
            ]
        }
        '''
        pass
    elif request.method == 'POST':
        # add a truck
        ''' VIEW RETURN EXAMPLE BELOW:
        {
            status: ""success"",
        }
        '''
        pass
    return make_response(IN_PROGRESS)
    
    
@app.route('/api/v1/trucks/assign/<id>', methods=['PUT'])
def assign_order(id):
    # assigns order balance to a truck
    if request.method == 'PUT':
        # assign order balance to a truck
        return make_response(IN_PROGRESS)


@app.route('/api/v1/trucks/<id>', methods=['GET'])
def get_truck(id):
    # get truck by id
    if request.method == 'GET':
        return make_response(IN_PROGRESS)


@app.route('/api/v1/trucks/available', methods=['GET'])
def get_available_trucks():
    # gets available trucks
    ''' VIEW RETURN EXAMPLE BELOW:
    {
        status: ""success"",
        data: 
        [
            {
                truckNo:""TT805"",
                licenseNo:""2005LP"",
                orderComps:["""","""","""","""","""",""""],
                sizeComps:[20,30,30,30,40,50],
                contractor:""Norman Manley""
            },
            {
                truckNo:""CJ9647"",
                licenseNo:""2006LQ"",
                orderComps:["""","""","""","""","""",""""],
                sizeComps:[20,30,30,30,40,50],
                contractor:""Alex Bustamante""
            },
            {
                truckNo:""JM2023"",
                licenseNo:""2007LR"",
                orderComps:["""","""","""","""","""",""""],
                sizeComps:[20,30,30,30,40,50],
                contractor:""Nanny Maroon""
            }
        ]
    }
    '''
    if request.method == 'GET':
        start = request.args.get('start')
        end = request.args.get('end')
        return make_response(IN_PROGRESS)
    return make_response(INVALID)


@app.route('/api/v1/trucks/booked', methods=['GET'])
def get_booked_trucks():
    # gets a list of booked truck objects
    ''' VIEW RETRUN EXAMPLE BELOW:
    {
        status: "success",
        data: 
        [
            {
                truckNo:"TT807",
                licenseNo:"2002LM",
                orderComps:["E10015","E10015","E10014","E10014","E10015","E10015"],
                sizeComps:[20,30,30,30,40,50],
                contractor"Paul Bogle"
            },
            {
                truckNo:"TT008B",
                licenseNo:"2003LN",
                orderComps:["","","","E10016","","E10016"],
                sizeComps:[20,30,30,30,40,50],
                contractor:"Marcus Garvey"
            },
            {
                truckNo:"00003"",
                licenseNo:"2004LO"",
                orderComps:["","","","","",""],
                sizeComps:[20,30,30,30,40,50],
                contractor:"Sam Sharpe"
            }
        ]
    }
    '''
    if request.method == 'GET':
        start=request.args.get('start')
        end=request.args.get('end')
        time=request.args.get('time')
        return make_response(IN_PROGRESS)
    return make_response(INVALID)


# USERS END POINTS 

@app.route('/api/v1/users', methods=['POST'])
def users():
    if request.method == 'POST':
        # add user
        return make_response(IN_PROGRESS)
    elif request.method == 'GET':
        # get all users
        return make_response(IN_PROGRESS)
    return make_response(INVALID)




# -- helper functions -- 

def min_order_value():
    # gets the minimum order quantity that can be fulfilled by the system
    return make_response(IN_PROGRESS)


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