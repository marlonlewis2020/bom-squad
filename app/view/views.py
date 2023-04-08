from app import app, db
from flask import Flask, url_for, redirect, flash, render_template, request, session, make_response
from model.models import Customer, User, Address
# from app.classes.Address import Address
# from app.classes.Admin import Admin
# from app.classes.Customer import Customer
# from app.classes.Driver import Driver
# from app.classes.Order import Order
# from app.classes.Report import Report
# from app.classes.Reservation import Reservation
# from app.classes.Schedule import Schedule
# from app.classes.Truck import Truck
# from app.classes.User import User

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

@app.route('/api/v1/customers/<id:int>', method=['GET','PUT'])
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
            
        customer = db.session.query(Customer)\
            .join(User, Customer.id==User.id)\
            .join(Address, Address.user_id==Customer.id)\
            .add_column(Customer.id, Customer.company, Customer.branch, Customer.officer, User.phone_number, User.email,Address.street, Address.city, Address.parish, Address.country)\
            .filter(customer.id==id).scalar()
        
        if customer is not None:    
            response = {
                'status':'success',
                'data':{
                    'customerID':customer.id,
                    'company':customer.company,
                    'branch':customer.branch,
                    'phoneNumber':customer.phone,
                    'email':customer.email,
                    'purchasingOfficer':customer.purchasingOfficer,
                    'location':customer.location
                    }
            }
        
        return make_response(response)
    elif request.method == 'PUT':
        # Update Customer details by customer id
        
        ''' VIEW RETURN EXAMPLE BELOW:
        '''
        return make_response(IN_PROGRESS)
    return make_response(INVALID)


@app.route('/api/v1/customers', method=['POST'])
def customers():
    #adds all the deatils of a customer
    if request.method == 'POST':
        ''' VIEW EXAMPLE OF PASSED PARAMS BELOW:
            company:"Total",
            branch:"Barbican",
            username:"total_barbican",
            password:"password123",
            role:"customer",
            phoneNumbers:["(876)-555-0555","(876)-555-1555"],
            email:"totalbarbican@gmail.com",
            purchasingOfficer:"Robert Desnoes",
            location:"12 Barbican Road, Barbican, St. Andrew, Ja."

        VIEW WXAMPLE OF RETURN VALUE BELOW:
        {
            status: "success"
        }
        '''
        return make_response(IN_PROGRESS)
    elif request.method=='GET':
        return make_response(IN_PROGRESS)
    return make_response(INVALID)
    

@app.route('/api/v1/customers/contact/<id:int>', method=['GET','POST', 'PUT'])
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

@app.route('/api/v1/orders/<id:int>', method=['GET', 'PUT'])
def order(id):
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
        pass
    elif request.method == 'PUT':
        # UPDATE THE ORDER DETAILS
        ''' VIEW RETURN EXAMPLE BELOW
        {
            status: "success"
        }
        '''
        pass
    return make_response(IN_PROGRESS)
    
    
@app.route('/api/v1/orders', method=['GET', 'POST'])
def orders(): 
    # gets all or adds an order
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
        pass
    elif request.method == 'POST':
        # adds an order
        ''' PARAMS EXAMPLE BELOW:
        "customerID: ""00000000""
        orderDate:<date:dateFormat>
        diesel: <quantity1:int>,
        87: <quantity2:int>,
        90: <quantity3:int>,
        ulsd: <quantity1:int>,
        location: <addressID>
        delivery: <date:dateFormat>"
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
        pass
    return make_response(IN_PROGRESS)


@app.route('/api/v1/orders/cancel/<id:int>', method=['GET'])
def cancel_order(id):
    # cancels an order by order id
    return make_response(IN_PROGRESS)


@app.route('/api/v1/orders/min-order-value', method=['GET'])
def min_order_value():
    # gets the minimum order quantity that can be fulfilled by the system
    return make_response(IN_PROGRESS)
    
    
@app.route('/api/v1/orders/schedule', method=['GET'])
def get_schedule():
    # start=<date:dateForma/t>&end=<date:dateFormat>
    start = request.args.get('start')
    end = request.args.get('end')
    return make_response(IN_PROGRESS)
    
    
# -- TRUCK END POINTS --

@app.route('/api/v1/trucks', method=['GET', 'POST'])
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
    
    
@app.route('/api/v1/trucks/assign/<id:int>', method=['PUT'])
def assign_order(id):
    # assigns order balance to a truck
    if request.method == 'PUT':
        # assign order balance to a truck
        return make_response(IN_PROGRESS)


@app.route('/api/v1/trucks/<id:int>', method=['GET'])
def get_truck(id):
    # get truck by id
    if request.method == 'GET':
        return make_response(IN_PROGRESS)


@app.route('/api/v1/trucks/available', method=['GET'])
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


@app.route('/api/v1/trucks/booked', method=['GET'])
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

@app.route('/api/v1/users', method=['POST'])
def users():
    if request.method == 'POST':
        # add user
        return make_response(IN_PROGRESS)
    elif request.method == 'GET':
        # get all users
        return make_response(IN_PROGRESS)
    return make_response(INVALID)




# -- helper functions -- 
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