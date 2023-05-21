# Author: Marlon Lewis
# ID: 620001669

from queue import Queue
from sqlalchemy import desc
from app import db
from app.models import DeliveryCompartment, Order, Area, Truck, Address, Delivery, Compartment
from datetime import datetime
from app.utils.utils import format_date, sql_date, strtodate
from app.utils.support.BinaryHeap import BinaryHeap as PQ

class Graph:
    # Class for Building Graph's Adjacency Matrix
    available_trucks = []
    INF = float("Inf")

    def __init__(self, customer_id, order, start_node, petrol, ord_qty, date, time, depth):
        """Graph Constructor
        """
        self.upgrade_pq = PQ() 
        self.customer_id = customer_id
        self.order_id = order
        self.petrol = petrol
        self.DEPTH = {}
        self.local_map = {}
        self.booked = []
        
        self.available_trucks = PQ() # priority on truck size
        self.booked_trucks = PQ() # priority on nearness value to qty
        self.AREAS = {} # Area Data and Trucks
        """
            {"Kingston": {"trucks":[], "available_space":0, "depth"=None }, 
            "St. Catherine": {"trucks":[], "available_space":60, "depth"=None }, 
            "Clarendon": {"trucks":[], "available_space":10, "depth"=None }, ...}
        """
        self.QTY = ord_qty
        self.O_QTY = ord_qty
        self.DEPTH['max_depth'] = depth
        self.DEPTH['current'] = 1
        self.start_node = start_node
        
        self.delivery_date = date
        self.delivery_time = time
        
        self.discovered = Queue()
        self.visited = []
        
    def get_this_date_time_deliveries(self):
        deliveries = db.session.query(Delivery).distinct()\
            .join(DeliveryCompartment, DeliveryCompartment.delivery_id==Delivery.id)\
            .filter((Delivery.date==self.delivery_date) & (Delivery.time==self.delivery_time)).all()
        return deliveries
        
    def load_area_nodes2(self):
        booked_ids = set()
        # 1. get all nodes
        parishes = set([x[0] for x in db.session.query(Area.area).distinct().all()+db.session.query(Area.neighbour).distinct().all()])
        nbrs = [(x.area, x.neighbour) for x in db.session.query(Area).all()]
        # 2. load map - areas - nbrs
        # 2.1 initialize the local_map with its unbooked trucks
        for parish in parishes:
            self.AREAS[parish] = {"trucks":[],"available_space":0}
            
            for n in nbrs:
                if parish in n:
                    nbr = 1 - n.index(parish)
                    if self.local_map.get(parish, None) is None:
                        self.local_map[parish] = [n[nbr]]
                    else:
                        if parish not in self.local_map[parish]:
                            self.local_map[parish].append(n[nbr])
                        
                    if self.local_map.get(n[nbr], None) is None:
                        self.local_map[n[nbr]] = [parish]
                    else:
                        if n[nbr] not in self.local_map[n[nbr]]:
                            self.local_map[n[nbr]].append(parish)
            # print(self.local_map.items())
                        
            # 2.2 load area - booked trucks
            deliveries = db.session.query(Delivery)\
            .join(DeliveryCompartment, DeliveryCompartment.delivery_id==Delivery.id)\
            .filter((Delivery.date==self.delivery_date) & (Delivery.time==self.delivery_time)
                & (DeliveryCompartment.parish==parish)).all()
            for delivery in deliveries:
                booked_ids.add(delivery.truck_id)
                self.AREAS[parish]['trucks'].append(db.session.query(Truck).filter_by(id=delivery.truck_id).scalar())
                self.AREAS[parish]['available_space'] += delivery.available

        # load unbooked trucks
        av_trucks = db.session.query(Truck).filter(~(Truck.id.in_(tuple(booked_ids)))).all()
        for av in av_trucks:
            pri = -av.capacity
            self.available_trucks.heap_insert((pri, av))
                           
    def discover( self ):
        # self.load_area_nodes2
        fringe = []
        fringe.append(self.start_node)
        while self.DEPTH['current'] < self.DEPTH['max_depth']:
            # get all the trucks from within the specified depth.\
            depth = self.DEPTH['current']-1
            if len(fringe) and len(fringe) >= depth:
                location = fringe[depth]
                nbrs = self.local_map.get(location, None)
                if nbrs:
                    for n in nbrs:
                        if n not in fringe:
                            fringe.append(n)
            else:
                continue
            self.DEPTH['current'] += 1
        return fringe

            
    def get_neighbours(self, area):
        return self.local_map.get(area, None)
    
        
    def fill_trucks(self):
        # get the available and booked trucks from db
        self.load_area_nodes2()
        
        # Are there existing delivery trucks for this customer/area that has available space to carry some of the order balance?
        d_prevs = db.session.query(Delivery).join(DeliveryCompartment, DeliveryCompartment.delivery_id==Delivery.id)\
            .join(Order, Order.id==DeliveryCompartment.order_id)\
            .filter((Order.status!="Delivering") & (Order.status!="Delivered") & (Order.customer_id==self.customer_id)
                & (Delivery.date==self.delivery_date) & (Delivery.time==self.delivery_time) & (DeliveryCompartment.parish==self.start_node)).all()
        # cycle = 0    
        if d_prevs:
            customer_other_orders = PQ()
            for deliv in d_prevs:
                if deliv.available>0 and self.QTY>=deliv.available:
                    pri = abs(self.QTY-deliv.available)
                    customer_other_orders.heap_insert((pri, deliv))
            while not customer_other_orders.empty():
                # if cycle >= 1: break
                d = customer_other_orders.pop()
                if d and self.QTY >= d.available:
                    t = db.session.query(Truck).filter_by(id=d.truck_id).scalar()
                    self.QTY = t.fill_each(self.order_id, self.QTY, self.petrol, self.delivery_date, self.delivery_time, self.start_node)
                    # cycle += 1
                
        
        # greedily fill order with available trucks
        # if order qty >= popped truck below
        truck = self.available_trucks.pop()
        if truck:
            while self.QTY >= truck.capacity:
                # fill truck
                self.QTY -= truck.fill_all( self.order_id, self.QTY, self.petrol, self.start_node, self.delivery_date, self.delivery_time)
                # update the original order qty
                self.QTY-=truck.capacity
                if self.QTY == 0:
                    break
                truck = self.available_trucks.pop()
                if not truck:
                    break
            # fill balance is left, fill booked trucks
            pq = self.find_best_fit()
            if pq.empty():
                pq = []
            else:
                ac = pq.pop().available_compartments(self.delivery_date, self.delivery_time)
                pq = [x.capacity for x in ac]
        return (self.QTY, pq)
    
    
    def find_best_fit( self):
        """Routine to discover and visit nodes in search for next best fit truck

        Args:
            depth (_type_): _description_
            qty (_type_): _description_
            location (_type_): _description_
            pop from booked trucks and add to upgrade queue
            
        """
        # fill existing booked delivery truck first
        priority_pq = PQ() # automatically fill order using this queue
        truck_list = [] # automatically fill order using this queue
        areas = self.discover()
        for a in areas:
            # get trucks from a and add them to up
            a_trucks = list(self.AREAS[a]['trucks'])
            # just throw them into the queue by available space
            for truck in a_trucks:
                priority_pq.heap_insert((-truck.available(self.delivery_date, self.delivery_time), truck))
        while not priority_pq.empty():
            b_truck = priority_pq.pop() # fill the remaining balance
            if b_truck and self.QTY >= b_truck.available(self.delivery_date, self.delivery_time):
                # fill order
                self.QTY = b_truck.fill_each(self.order_id, self.QTY, self.petrol, self.delivery_date, self.delivery_time, self.start_node)
                db.session.commit()
                if b_truck.available(self.delivery_date, self.delivery_time) > 0 and self.QTY>0 and b_truck not in truck_list: 
                    truck_list.append(b_truck)
        
        # add remaining trucks into upgrade queue
        # FILL THE COMPARTMENTS OF THE AVAILABLE TRUCKS CLOSEST IN SIZE TO THE ORDER SIZE
        if not self.available_trucks.empty() and self.QTY > 0:
            truck = self.available_trucks.pop()
            if truck and truck.available(self.delivery_date, self.delivery_time):
                db.session.rollback()
                db.session.flush()
                # check for existing_delivery
                # find existing delivery truck with same order number that has available space.
                et = db.session.query(Delivery).join(DeliveryCompartment, Delivery.id==DeliveryCompartment.delivery_id)\
                    .filter((DeliveryCompartment.order_id==self.order_id) & (Delivery.date==self.delivery_date) & (Delivery.time==self.delivery_time) &(Delivery.available>0)).first()
                    
                # If the available space of existing delivery truck is smaller than the selected truck then choose the smaller for efficient use of resources (use the existing delivery truck).
                if et and et.available and et.available < truck.available(self.delivery_date, self.delivery_time):
                    truck_list.append(truck) # the larger truck is a possible truck to suggest as an upgrade later
                    truck = db.session.query(Truck).filter_by(id=et.truck_id).scalar()
                    self.QTY = truck.fill_each(self.order_id, self.QTY, self.petrol, self.delivery_date, self.delivery_time, self.start_node)
                    if truck.available(self.delivery_date, self.delivery_time) > 0 and self.QTY>0 and truck not in truck_list: 
                        truck_list.append(truck)
                else:
                    if self.QTY < truck.available(self.delivery_date, self.delivery_time):
                        self.QTY = truck.fill_each(self.order_id, self.QTY, self.petrol, self.delivery_date, self.delivery_time, self.start_node)
                        if truck.available(self.delivery_date, self.delivery_time) > 0 and self.QTY>0 and truck not in truck_list: 
                            truck_list.append(truck)
                    else:
                        self.QTY -= truck.fill_all(self.order_id, self.QTY, self.petrol, self.start_node, self.delivery_date, self.delivery_time)
                
                if self.QTY > 0:
                    pri = abs(self.QTY-truck.available(self.delivery_date, self.delivery_time))
                    self.upgrade_pq.heap_insert((pri, truck))
        
        # check for and add the remaining popped unbooked and available booked trucks that need to be added to the upgrade_pq queue of order/truck upgrade suggestions            
        if len(truck_list):
            for truck in truck_list:
                if truck.available(self.delivery_date, self.delivery_time):
                    pri = abs(self.QTY-truck.available(self.delivery_date, self.delivery_time))
                    self.upgrade_pq.heap_insert((pri, truck))
        return self.upgrade_pq
            
    
if __name__=="__main__":
    g = Graph("F")
    
