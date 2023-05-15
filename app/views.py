from datetime import datetime
from MySQLdb import IntegrityError
from app import app, db
from flask import Flask, url_for, redirect, request, session, make_response
from .models import Customer, User, Address, Order, Delivery, Area, Truck, Compartments
from .forms import CustomerForm, AddressForm, OrderForm, UserForm
from werkzeug.security import generate_password_hash
from app.utils.utils import strtodate, sql_date
from queue import PriorityQueue, Queue
from app.utils.support.Graph import Graph


ORDER_QUEUE = Queue()
    
IN_PROGRESS = {
    'status': 'error',
    'message': 'In progress!'
}

INVALID = {
    'status': 'error',
    'message': 'Invalid method!'
}

# # # -- End-Points -- # # #

# -- CUSTOMER END POINTS -- 

@app.route('/api/v1/customers/<id>', methods=['GET','PUT'])
def customer(id):
    """ Gets a customer's details """
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
                phoneNumber:"(876)-555-0555",
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
        response = {
            "status":"error",
            "message":"unable to update customer details"
        }
        form = CustomerForm()
        cus = db.session.query(Customer, User).filter(Customer.id==id).scalar()
        try:
            cus.address_id = form.address_id.data
            cus.company = form.company.data
            cus.branch = form.branch.data
            cus.officer = form.officer.data
            cus.name = form.name.data
            cus.contact_number = form.contact_number.data
            cus.email = form.email.data
            cus.role = form.role.data
            cus.username = form.username.data
            cus.password = generate_password_hash(form.password.data)
            db.session.add(cus)
            db.session.commit()
            response = {
                "status":"success"
            }
        except Exception as e:
            print(e)
            db.session.rollback()
        return make_response(response)
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
            address = Address(address[0].strip(), address[1].strip(), address[2].strip())
        elif len(address)==4:
            address = Address(address[0].strip(), address[1].strip(), address[2].strip(), address[3].strip())
        elif len(address)==5:
            address = Address(address[0].strip(), address[1].strip(), address[2].strip(), address[3].strip(), address[4].strip())
            
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
        customer = db.session.query(Address, Customer, User, Order)\
            .filter(
                (Address.id==Customer.address_id)\
                & (Customer.id==User.id)\
                & (User.id==Order.customer_id)\
                & (Order.id==id)).first()
        
        address = "{0} {1}, {2}, {3}, {4}".format(customer.Address.address_line_1, customer.Address.city, customer.Address.parish, customer.Address.country, customer.Address.postal_code)
        response = Order.to_json( customer.Order, customer.User.name, address )
        
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
    """Retrieves all orders or adds an order depending on the HTTP REST verbs (GET, POST)

    Returns:
        json: a json response with status and relevant states
    """
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
            "data":[]
        }
        orders = db.session.query(Order, Customer, Address, User)\
            .filter(
                (Order.customer_id==User.id)\
            & (User.id==Customer.id)\
            & (Customer.address_id==Address.id))\
            .all()
        for o in orders:
            response['data'].append(Order.to_json(o.Order, o.User.name, '{} {}, {}, {}, {}'.format(o.Address.address_line_1, o.Address.city, o.Address.parish, o.Address.country, o.Address.postal_code)))
        response["status"]="success"
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
        added = False
        
        # use best fit to fill the 
        try:
            cid = form.customer_id.data
            d_date = form.delivery_date.data
            d_time = form.delivery_time.data
            q = form.quantity.data
            qd = form.q_diesel.data
            q87 = form.q_87.data
            q90 = form.q_90.data
            qul = form.q_ulsd.data
            price = float(form.price.data)
            status = form.status.data
            balance = 0
            order = Order(None, cid, d_date, d_time, q, qd, q87, q90, qul, price, status)
            db.session.add(order)
            db.session.commit()
            db.session.refresh(order)
            added = True
            
            # critical operation: book trucks and fill compartments to best match order (just under or equal to original order amount)
            # keek waiting until critical operation have been performed/completed            
            # async/sequential operation on database
            ORDER_QUEUE.put(order.id)
            while not ORDER_QUEUE.empty() and ORDER_QUEUE.queue[0] != order.id:
                continue
            
            """ Perform critical operations """
            address = db.session.query(Address).filter_by(id=form.location.data).first()
            q_diesel_order = Graph(address.parish, qd, d_date, 10)
            q_87_order = Graph(address.parish, q87, d_date, 10)
            q_90_order = Graph(address.parish, q90, d_date, 10)
            q_ulsd_order = Graph(address.parish, qul, d_date, 10)
            total_order = {
                "q_diesel_order" : q_diesel_order,
                "q_87_order" : q_87_order,
                "q_90_order" : q_90_order,
                "q_ulsd_order" : q_ulsd_order
            }
            
            i_orders = total_order.keys()
                
            for gas in i_orders:
                fill_order = total_order[gas]
                result = fill_order.fill_trucks(order, fill_order.QTY, address)
            
            # get the filled qtys and update order qty's accordingly
    
            # update the balance variable with the upgrade balance
            
            # update the existing order using order object
            
            # release lock
            ORDER_QUEUE.get()
            
            # for truck in trucks:
                
            db.session.commit()
            response = {
                "status": "success",
                "ordr_filled":q,
                "upgrade_amount":balance
            }
        except Exception as e:
            print(e)
            # remove order id
            if not ORDER_QUEUE.empty():
                ORDER_QUEUE.get()
            db.session.rollback()
            if added:
                db.session.delete(order)
                db.session.commit()
                response['message'] = "Unable to add order."
        
    return make_response(response)

@app.route('/api/v1/orders/<id>', methods=['POST'])
def confirm_order(id, upgrade=False):
    """Confirm a pending order"""
    # if upgrade, assign the compartment for the truck in the global variable to this order id, and update the truck compartment's capacity
    # free up lock on table reords in global variable , and remove the order details from the global variable
    # i.e. locked_trucks_by_ids = {order_id:{'truck_id':1000,'compartment_ids':[2,3]}, order_id:{'truck_id':1001,'compartment_ids':[3]} # lock only 1 truck per order for upgrade
    # update the order qty's for the order based, if necessary
    # if popped truck is already locked, keep popping until a truck that isn't globally locked is found
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