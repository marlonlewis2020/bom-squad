from datetime import datetime, timedelta
import MySQLdb
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, LOCKED, PEND, login_manager
from flask import Flask, jsonify, request, session, make_response

from app.utils.support.BinaryHeap import BinaryHeap
from .models import Customer, User, Address, Order, Delivery, Area, Truck, Compartment, DeliveryCompartment
from .forms import CustomerForm, AddressForm, OrderForm, UserForm, TruckForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.utils import format_date, sql_date, strtodate
from queue import Queue
# from app.utils.support.Graph import Graph
from app.utils.support.G import Graph
import jwt

ACTIVE = {}
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

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.method=="POST":
        try:
            data = LoginForm()
            username = data.username.data
            password = data.password.data
            timestamp= datetime.utcnow()
            expiry_date= timestamp+timedelta(days=7)
            user = User.query.filter_by(username=username).first()
            print(user)
            if user is not None and check_password_hash(user.password, password):
                payload = {'sub': user.id, "iat":timestamp, "exp": expiry_date}
                
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm = 'HS256')
                if login_user(user):
                    load_user(user.id)
                return jsonify(status='success', message = 'User successfully logged in.', id=user.id, token=token)
            return jsonify(errors="Invalid username or password")
        except Exception as e:
            print(e)
            return jsonify(errors='An error occurred while processing your request'), 500
    return jsonify(errors='Invalid request method'), 405



@app.route('/api/v1/auth/logout', methods = ['POST','GET'])
@login_required
def logout():
    token = request.headers.get('Authorization', None).split(" ")
    try:
        if user_authorized() and len(token) == 2 and token[0].lower() == "bearer":
            payload = jwt.decode(token[1], app.config['SECRET_KEY'], algorithms=['HS256'])
            user = ACTIVE.get(payload.get('sub'), None)
            role = ACTIVE.get(payload.get('role'), None)
            if user is not None:
                ACTIVE.pop(user.id)
            logout_user()
        return jsonify(status="success", message = "User sucessfully logged out."), 200
    except Exception as e:
        print(e)
        return jsonify(errors='An error occurred while processing your request'), 500
    
@app.route("/api/v1/generate-token")
@login_required
def generate_token():
    timestamp = datetime.utcnow()
    if current_user is not None:
        payload = {
            "sub": current_user.id,
            "role": current_user.role,
            "iat": timestamp,
            "exp": timestamp + timedelta(days=7)
        }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify(token=token)

# -- CUSTOMER END POINTS -- 

@app.route('/api/v1/customers/<id>', methods=['GET','PUT'])
# @login_required
def customer(id):
    """ Gets or updates a customer's details """
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
                    'customer_id':customer.id,
                    'company':customer.company,
                    'branch':customer.branch,
                    'contact_number':customer.contact_number,
                    'email':customer.email,
                    'officer':customer.officer,
                    'location':address,
                    'address_id':location.id
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
            "message":"unable to update customer details."
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
            # cus.username = form.username.data
            cus.password = generate_password_hash(form.password.data)
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
        
        if form.location.data:
            address = form.location.data
        else:
            address = "{},{},{},{},{}".format(form.address_line_1.data.strip(), form.city.data.strip(), form.parish.data.strip(), form.country.data.strip(), form.postal_code.data.strip())
            
        address=address.split(",")
        
        # address = Address()
        # address.address_line_1 = form.address_line_1.data.strip()
        # address.city = form.city.data.strip()
        # address.parish = form.parish.data.strip()
        # address.country = form.country.data.strip()
        # address.postal_code = form.postal_code.data.strip()
        address = Address(address[0].strip(), address[1].strip(), address[2].strip(), address[3].strip(), address[4].strip())
        # if len(address)==3:
        #     address = Address(address[0].strip(), address[1].strip(), address[2].strip())
        # elif len(address)==4:
        #     address = Address(address[0].strip(), address[1].strip(), address[2].strip(), address[3].strip())
        # elif len(address)==5:
        #     address = Address(address[0].strip(), address[1].strip(), address[2].strip(), address[3].strip(), address[4].strip())
            
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
            
        except Exception as e:
            print (e)
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
# @login_required
def order(id):
    response = IN_PROGRESS
    # gets or updates an order
    if request.method == 'GET':
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
        try:
            customer = db.session.query(Address, Customer, User, Order)\
                .filter(
                    (Address.id==Customer.address_id)\
                    & (Customer.id==User.id)\
                    & (User.id==Order.customer_id)\
                    & (Order.id==id)).first()
            
            address = "{0} {1}, {2}, {3}, {4}".format(customer.Address.address_line_1, customer.Address.city, customer.Address.parish, customer.Address.country, customer.Address.postal_code)
            response = Order.to_json( customer.Order, customer.User.name, address )
        except Exception as e:
            print(e)
            response = {
                "status":"error",
                "message":"Order (#{}) not found.".format(id)
            }
    elif request.method == 'PUT':
        # UPDATE THE ORDER DETAILS
        ''' VIEW RETURN EXAMPLE BELOW
        {
            status: "success"
        }
        '''
        try:
                
            form = OrderForm()
            order=db.session.query(Order).filter_by(id=id).first()
            order.delivery_date = strtodate(form.delivery_date.data)
            order.last_updated = datetime.utcnow()
            order.delivery_time = form.delivery_time.data
            order.quantity = form.quantity.data
            order.q_diesel = form.q_diesel.data
            order.q_87 = form.q_87.data
            order.q_90 = form.q_90.data
            order.q_ulsd = form.q_ulsd.data
            order.price = form.price.data
            order.status = "Pending"
            # update order object
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            response = {
                "status":"error",
                "message":"unable to update order"
            }
        response = {
            "status": "success"
        }
    return make_response(response)
    
    
@app.route('/api/v1/orders', methods=['GET', 'POST'])
# @login_required
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
        try:    
            orders = db.session.query(Order, Customer, Address, User)\
                .filter(
                    (Order.customer_id==User.id)\
                & (User.id==Customer.id)\
                & (Customer.address_id==Address.id)\
                & (Order.status != "Cancelled")\
                & (Order.status != "Deleted"))\
                .all()
            for o in orders:
                response['data'].append(Order.to_json(o.Order, o.User.name, '{} {}, {}, {}, {}'.format(o.Address.address_line_1, o.Address.city, o.Address.parish, o.Address.country, o.Address.postal_code)))
            response["status"]="success"
        except Exception as e:
            print(e)
            response['message'] = "Could not generate list of orders"
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
        balance = {}
        # added = False
        
        # use best fit to fill the 
        try:
            cid = int(form.customer_id.data)
            d_d = form.delivery_date.data.strip()
            d_time = form.delivery_time.data.strip()
            qd = int(form.q_diesel.data)
            q87 = int(form.q_87.data)
            q90 = int(form.q_90.data)
            qul = int(form.q_ulsd.data)
            q = qd+q87+q90+qul          
            price = float(form.price.data)
            status = form.status.data
            d_date = ""
            if len(d_d.split("-"))==3:
                d_date = format_date(datetime(*[int(x) for x in d_d.split("-")]))
            else:
                d_date = d_d[0]
            order = Order(None, cid, d_date, d_time, 0, 0, 0, 0, 0, price, status)
            db.session.add(order)
            db.session.commit()
            db.session.refresh(order)
            # added = True
            
            # critical operation: book trucks and fill compartments to best match order (just under or equal to original order amount)
            # keek waiting until critical operation have been performed/completed            
            # async/sequential operation on database
            ORDER_QUEUE.put(order.id)
            while not ORDER_QUEUE.empty() and ORDER_QUEUE.queue[0] != order.id:
                continue
            
            """ Perform critical operations """
            address = db.session.query(Address).filter_by(id=int(form.location.data)).first()
            q_diesel_order = Graph(order.id, address.parish, "diesel", qd, d_date, d_time, 10)
            q_87_order = Graph(order.id, address.parish, "87", q87, d_date, d_time, 10)
            q_90_order = Graph(order.id, address.parish, "90", q90, d_date, d_time, 10)
            q_ulsd_order = Graph(order.id, address.parish, "ulsd", qul, d_date, d_time, 10)
            total_order = {
                "q_diesel_order" : q_diesel_order,
                "q_87_order" : q_87_order,
                "q_90_order" : q_90_order,
                "q_ulsd_order" : q_ulsd_order
            }
            
            preferred = f"q_{form.preferred.data}_order"
            prioritized_order = BinaryHeap()
            i_orders = total_order.keys()
            total_left = 0
            for gas in i_orders:
                sub_order = total_order[gas]
                if gas == preferred:
                    prioritized_order.heap_insert((0, sub_order))
                else:
                    prioritized_order.heap_insert((1, sub_order))
                    
            while not prioritized_order.empty():
                sub_order = prioritized_order.pop()
                if sub_order.QTY > 0:
                    result = sub_order.fill_trucks()
                    total_left += result[0]
                    balance[gas]={
                        "ordered":sub_order.O_QTY,
                        "filled":sub_order.O_QTY-result[0],
                    }
                    
                    if str(gas.split("_")[1]).strip() == form.preferred.data.strip():
                        balance[gas]["upgrades"]=result[1]
            
            # get the filled qtys and update order qty's accordingly
            # update the balance variable with the upgrade balance
    
            
            # update the existing order using order object
            
            # release lock
            ORDER_QUEUE.get()
            
            # for truck in trucks:
                
            db.session.commit()
            response = {
                "status":"success",
                "ordered":q,
                "order_filled":q-total_left,
                "options":balance
            }
            if q==total_left:
                # order cannot be filled. No trucks are available for the date
                db.session.delete(order)
                db.session.commit()
                response["status"] = "error"
                response["message"] = "unable to fulfill order at this time. Please try a different date."
            else:
                for gas in i_orders:
                    fill_order = total_order[gas]
                    if str(form.preferred.data).strip().casefold() == str(gas.split("_")[1]).casefold().strip():
                        if not fill_order.upgrade_pq.empty():
                            ug = fill_order.upgrade_pq.pop()
                            lock_truck(order.id, ug, gas)
        except MySQLdb.OperationalError as ope:
            print(ope)
        
        except Exception as e:
            print(e)
            # remove order id
            if not ORDER_QUEUE.empty():
                ORDER_QUEUE.get()
            db.session.rollback()
            db.session.delete(order)
            response = {
                "status":"error"
            }
            response['message'] = "Unable to add order."
            # if added:
                # db.session.delete(order)
                # db.session.commit()
        
    return make_response(response)

@app.route('/api/v1/orders/<id>', methods=['POST'])
# @login_required
def confirm_order(id):
    """Confirm a pending order"""
    if request.method=="POST":
        response = {
            "status":"error",
            "message":"could not upgrade order. Please contact customer service for support."
        }
        truck_id = PEND.get(int(id), None)
        truck = db.session.query(Truck).filter_by(id=truck_id).first()
        if truck_id:
            data = LOCKED.get(truck_id, None)
            if data is not None:
                gases = [ "q_diesel_order", "q_87_order", "q_90_order", "q_ulsd_order" ]
                try:    
                    order = db.session.query(Order, Delivery, Truck).filter((Order.id==id) & (Order.id==Delivery.order_id) & (Truck.id==Delivery.truck_id)).first()
                    for i, gas in enumerate(gases):
                        # get amount to upgrade this gas type by from the response and update the compartment
                        amount = int(request.form.get(gas.split("_order")[0]))
                        comps = truck.available_compartments()
                        
                        for comp in comps:
                            # fill all compartments of this truck
                            if comp.capacity == amount:
                                delivery = db.session.query(DeliveryCompartment).filter_by(truck_id=truck_id).first()
                                comp = DeliveryCompartment( delivery.id, id, comp.id, truck_id, gas, comp.capacity)
                                db.session.add(comp)
                        match gas:
                            # update the specific fuel type quantity
                            case "diesel":
                                order.q_diesel += amount
                            case "87":
                                order.q_87 += amount
                            case "90":
                                order.q_90 += amount
                            case "ulsd":
                                order.q_ulsd += amount
                        # update the total order quantity
                        order.quantity += amount
                                            
                    # update the entire truck status from PENDING 
                    order.status = "Ready"
                    order.last_updated = datetime.utcnow()
                    db.session.commit()
                    response = {
                        "status":"success"
                    }
                except Exception as e:
                    print(e)
                    db.session.rollback()
            # unlock truck
            unlock_truck(order.Order.id)
        return make_response(response)
    return make_response(INVALID)
            

@app.route('/api/v1/cancel/<id>', methods=['POST'])
# @login_required
def cancel_order(id):
    """Cancels the order"""
    response = {
        "status":"error",
        "message":"could not cancel order"
    }
    try:
        order = db.session.query(Order).filter_by(id=id).first()
        if order.status not in ["Delivered", "Cancelled"]:
            deliveries = db.session.query(Delivery).distinct().filter(
                (Delivery.order_id==id)).all()
            
            for d in deliveries:
                db.session.delete(d)
                # use truck id to get truck
                truck = db.session.query(Truck).filter((Truck.id==d.truck_id) & (Truck.available<Truck.capacity)).first()
                if truck is not None:
                    truck.available = truck.capacity
                    # set truck's available column to capacity
                    # use truck id to get the compartments with order id = id
                    comps = db.session.query(Compartment).filter((Compartment.truck_id==d.truck_id) & (Compartment.order_id==id)).all()
                    for c in comps:
                        # remove petrol value from compartment
                        c.petrol=""
                        # remove order id from comp
                        c.order_id=0
            # mark order as delivered
            order.status = "Cancelled"
            # update order's last_updated field
            order.last_updated = datetime.utcnow()
            db.session.commit()
            
            response = {
                "status":"success"
            }
        else:
            response['message'] = f"Order {id} already cancelled."
    except Exception as e:
        print(e)
        db.session.rollback()
    
    return make_response(response)
    
    
@app.route('/api/v1/orders/schedule', methods=['POST'])
# @login_required
def get_schedule():
    # start=<date:dateForma/t>&end=<date:dateFormat>
    date = request.form.get('date')
    time = request.form.get('time')
    
    response = {
        "data":{}
    }
    try:    
        orders = db.session.query(Order, Customer, Address, User)\
            .filter(
                (Order.customer_id==User.id)\
            & (User.id==Customer.id)\
            & (Customer.address_id==Address.id)\
            & (Order.delivery_date >= sql_date(strtodate(date)))\
            & (Order.status != "Pending")\
            & (Order.status != "Cancelled")\
            & (Order.status != "Deleted"))\
            .all()
        for o in orders:
            if response['data'].get(format_date(o.Order.delivery_date), None):
                response['data'][format_date(o.Order.delivery_date)].append(Order.to_json(o.Order, o.User.name, '{} {}, {}, {}, {}'.format(o.Address.address_line_1, o.Address.city, o.Address.parish, o.Address.country, o.Address.postal_code)))
            else:
                response['data'][format_date(o.Order.delivery_date)] = []
                response['data'][format_date(o.Order.delivery_date)].append(Order.to_json(o.Order, o.User.name, '{} {}, {}, {}, {}'.format(o.Address.address_line_1, o.Address.city, o.Address.parish, o.Address.country, o.Address.postal_code)))
        response["status"]="success"
    except Exception as e:
        print(e)
        response = {
            "status":"success"
        }
        response['message'] = "Could not generate list of orders"
    return make_response(response)
    
    
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
        response = {
            "status":"error",
            "message":"unable to add new truck."
        }
        try:
            form = TruckForm()
            truck = Truck(form.license_plate.data, form.capacity.data, form.make.data, form.model.data, form.year.data, form.active.data)
            db.session.add(truck)
            db.session.commit()
            db.session.refresh(truck)
            
            cap = [int(x) for x in form.capacity.data.split(",")]
            for i, capacity in enumerate(cap):
                compartment_no = i+1
                comp = Compartment(truck.id, compartment_no, capacity)
                db.session.add(comp)
            db.session.commit()
            response = {
                "status":"success"
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            
        return make_response(response)
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


@app.route('/api/v1/trucks/available', methods=['POST'])
def get_available_trucks():
    """ Lists all unbooked trucks """
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
    response = {
        "status":"success",
        "message":"could not generate list of available trucks."
    }
    if request.method == 'POST':
        
        date = request.form.get('date')
        time = request.form.get('time')
        try:
            truck_ids = db.session.query(Delivery.truck_id).distinct().join(Order, Order.id==Delivery.order_id).filter(
                (Delivery.date==date) & (Delivery.time==time) & (Order.status!="Cancelled") & (Order.status!="Delivered")).all()
            truck_ids = [x.truck_id for x in truck_ids]
            available_trucks = db.session.query(Truck).filter(~Truck.id.in_(tuple(truck_ids))).filter((Truck.active==1) & (Truck.available>0)).all()
            
            response = {
                "status":"success",
                "available_trucks":[x.repr() for x in available_trucks]
            }
        except Exception as e:
            print(e)
            
        return make_response(response)
    return make_response(INVALID)


@app.route('/api/v1/trucks/booked', methods=['POST'])
def get_booked_trucks():
    """gets a list of booked truck objects"""
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
                contractor:"Paul Bogle"
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
    if request.method == 'POST':
        response = {
            "status":"error",
            "message":"Could not get the booked trucks."
        }
        try:
            date = request.form.get('date')
            time = request.form.get('time')
            truck_ids = db.session.query(Delivery.truck_id).distinct().filter(
                (Delivery.date==date) & (Delivery.time==time) ).all()
            truck_ids = [x.truck_id for x in truck_ids]
            
            trucks = db.session.query(Truck).filter(Truck.id.in_(tuple(truck_ids)))\
            .filter((Truck.active==1) & (Truck.available>=0)).all()
            
            available_booked_trucks = db.session.query(Truck).filter(Truck.id.in_(tuple(truck_ids)))\
            .filter((Truck.active==1) & (Truck.available>0)).all()
            
            response = {
                "status":"success",
                "all_booked_trucks":[x.repr() for x in trucks],
                "available_booked_trucks":[x.repr() for x in available_booked_trucks]
            }
        except Exception as e:
            print(e)
            
        return make_response(response)
    return make_response(INVALID)


# USERS END POINTS 

@app.route('/api/v1/users', methods=['GET'])
# @login_required
def users():
    response = {
        "status":"error"
    }
    if request.method == 'GET':
        # get all users
        try:
            users = db.session.query(User).all()
            response = {
                "status":"success",
                "users":[x.repr() for x in users]
            }
        except Exception as e:
            print(e)
            response['message'] = "Could not get users list."
        return make_response(response)
    return make_response(INVALID)


# -- helper functions -- 

def user_authorized():
    token = request.headers.get('Authorization', None)
    parts = []
    if token is not None: parts = token.split()
    if len(parts)==2 and parts[0].lower()=="bearer":
        payload = jwt.decode(parts[1], app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = payload['sub']
        if not current_user.is_authenticated and ACTIVE.get('user_id', None) is None:
            user = User.query.filter_by(id=user_id).first()
            if login_user(user):
                load_user(user_id)
                return True
            return False
        return True
    else:
        return False
    
@login_manager.user_loader
def load_user(id):
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar()
    if user is not None:
        ACTIVE[id] = user
    return user

def lock_truck(order_id, truck_id, gas):
    if not is_truck_locked(truck_id):
        LOCKED[truck_id] = {
            "gas":gas
        }
        PEND[order_id] = truck_id
    return (True, False) [not LOCKED.get(truck_id, False)]

def unlock_truck(order_id):
    truck_id = PEND.pop(order_id, True)
    LOCKED.pop(truck_id, True)
    return (True, False) [LOCKED.get(truck_id, False)]

def is_truck_locked(truck_id):
    return (True, False) [not LOCKED.get(truck_id, False)]


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
    response = {
        "status":"error",
        "message":"page not found."
    }
    return make_response(response, 404)

@app.errorhandler(405)
def page_not_found(error):
    """Custom 405 page."""
    response = {
        "status":"error",
        "message":"you are not logged in."
    }
    return make_response(response, 405)