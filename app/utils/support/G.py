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

    def __init__(self, order, start_node, petrol, ord_qty, date, time, depth):
        """Graph Constructor
        """
        self.upgrade_pq = PQ() 
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
            deliveries = db.session.query(Delivery).distinct()\
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
        #
        # greedily fill order with available trucks
        # if order qty >= popped truck below
        truck = self.available_trucks.pop()
        if truck:
            while self.QTY >= truck.capacity:
                # fill truck
                filled = truck.fill_all( self.order_id, self.petrol, self.start_node, self.delivery_date, self.delivery_time)
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
                ac = pq.pop().available_compartments()
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
                priority_pq.heap_insert((-truck.available(), truck))
        while not priority_pq.empty():
            b_truck = priority_pq.pop() # fill the remaining balance
            if b_truck:
                if self.QTY >= b_truck.available():
                    # fill order
                    balance = b_truck.available()
                    try:
                        order = db.session.query(Order).filter_by(id=self.order_id).scalar()
                        # get existing delivery
                        delivery = db.session.query(Delivery).filter(Delivery.truck_id==b_truck.id).first()
                        delivery.filled += balance
                        delivery.available -= balance
                        # delivery = Delivery(self.order_id, self.petrol, self.delivery_date, self.delivery_time, b_truck.id, self.start_node, balance, 0)
                        db.session.add(delivery)
                        db.session.commit()
                        created = True
                        db.session.refresh(delivery)
                        
                        d_comps = b_truck.available_compartments()
                        for comp in d_comps:
                            # fill all compartments of this truck
                            comp = DeliveryCompartment(delivery.id, self.order_id, comp.id, self.start_node, self.petrol, comp.capacity)
                            db.session.add(comp)
                        match self.petrol:
                            # update the specific fuel type quantity
                            case "diesel":
                                order.q_diesel += balance
                            case "87":
                                order.q_87 += balance
                            case "90":
                                order.q_90 += balance
                            case "ulsd":
                                order.q_ulsd += balance
                        # update the total order quantity
                        order.quantity += balance
                        db.session.commit()
                    except Exception as e:
                        created = False
                        print(e)
                        truck_list.append(b_truck)
                        if created:
                            db.session.delete(delivery)
                            db.session.commit()
                            db.session.rollback()
                else:
                    self.QTY = b_truck.fill_each(self.order_id, self.QTY, self.petrol, self.delivery_date, self.delivery_time, self.start_node)
                    if b_truck.available() > 0 and b_truck not in truck_list: truck_list.append(b_truck)
        
        # add remaining trucks into upgrade queue
        # FILL THE COMPARTMENTS OF THE AVAILABLE TRUCKS CLOSEST IN SIZE TO THE ORDER SIZE
        if not self.available_trucks.empty() and self.QTY > 0:
            truck = self.available_trucks.pop()
            if truck:
                db.session.rollback()
                db.session.flush()
                # existing_delivery
                # find delivery truck with same order number that has available space.case
                # If the available space is closer than the selected truck then use it.
                et = db.session.query(Delivery).join(DeliveryCompartment, Delivery.id==DeliveryCompartment.delivery_id)\
                    .filter((DeliveryCompartment.order_id==self.order_id) & (Delivery.available>0)).first()
                if et and et.available < truck.available():
                    truck = db.session.query(Truck).filter_by(id=et.truck_id).scalar()
                    self.QTY = truck.fill_each(self.order_id, self.QTY, self.petrol, self.delivery_date, self.delivery_time, self.start_node)
                else:
                    self.QTY -= truck.fill_all(self.order_id, self.petrol, self.start_node, self.delivery_date, self.delivery_time)
                
                if self.QTY > 0:
                    pri = abs(self.QTY-truck.available())
                    self.upgrade_pq.heap_insert((pri, truck.available()))
                    
                    if len(truck_list):
                        for truck in truck_list:
                            pri = abs(self.QTY-truck.available())
                            self.upgrade_pq.heap_insert((pri, truck.available()))
        return self.upgrade_pq
            
    
if __name__=="__main__":
    g = Graph("F")
    
