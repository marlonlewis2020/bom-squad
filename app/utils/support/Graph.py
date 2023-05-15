# Author: Marlon Lewis
# ID: 620001669

from queue import PriorityQueue

from sqlalchemy import desc
from app import db
from app.models import Order, Area, Truck, Address, Delivery, Compartments
from datetime import datetime
from app.utils.utils import format_date, sql_date, strtodate

class Graph:
    # Class for Building Graph's Adjacency Matrix
    available_trucks = []
    INF = float("Inf")

    def __init__(self, start_node, petrol, ord_qty, date, time, depth, last=False):
        """Graph Constructor
        """
        self.petrol = petrol
        self.last = last
        self.DEPTH = {}
        self.discovered = {}
        self.adjacency_list = {}
        self.booked_areas = PriorityQueue()
        self.AREAS = {} # Area Data and Trucks
        """{"Kingston": { "id":1, "node":{}, "trucks":[], "available_space":0 }, 
        "St. Catherine": { "id":2, "node":{}, "trucks":[], "available_space":60 }, 
        "Clarendon": { "id":3, "node":{}, "trucks":[], "available_space":10 }, ...}"""
        self.NBRS = [] # Edges depicting space available
        """[ (0, (None, "Kingston")), (1, ("Kingston", "St. Catherine")), (1, ("Kingston", "Clarendon")),
        (1, ("St.Catherine", "Clarendon")), (3, ("St. Catherine", "Manchester")), ... ]"""
        self.QTY = ord_qty
        self.DEPTH['max_depth'] = depth
        self.DEPTH[start_node] = 1
        self.start_node = start_node
        self.visited = []
        self.areas_in_depth = list() # list for: areas in which to look for booked trucks with space to fill other order balances
        self.excess = list()
        self.delivery_date = date
        self.delivery_time = time
        self.load_area_nodes()
        locations = list(self.AREAS.keys())
        
        # get the booked areas (based on orders made) and initialize them
        for area in locations:
            # initialize discovered, adjacency list
            self.discovered[area] = self.INF
            self.adjacency_list[area] = []
        
        # update the initialized areas with accurate data in adjacency list
        for area in locations:
            nbrs = self.neighbours(area)
            for i, nbr in enumerate(nbrs):
                if nbr == None: continue
                # print(self.adjacency_list[nbr], i)
                self.adjacency_list[area].append(nbr) 

        
    def reset(self):
        """Reset all variables"""
        self.QTY = 0
        self.DEPTH = {}
        self.load_area_nodes()
        self.visited = []
        self.areas_in_depth = list()
        self.excess = list()
        
    def load_area_nodes(self):
        """Load up the graph data structure - contains areas and the trucks booked for each area"""
        # date = sql_date(strtodate(self.delivery_date))  
        # time = self.delivery_time
        
        # get all deliveries scheduled for this delivery date     
        deliveries = self.get_deliveries()
        parishes = [x[0] for x in deliveries]
        truck_ids = [x[1] for x in deliveries]
        address_ids = [x[2] for x in deliveries]
        
        # get and loads areas and their neighbours
        # only get Areas where they have Orders on that date
        all_area_nbrs = db.session.query(Area).filter(Area.area.in_(tuple(parishes))).all() 
        
        #add areas and nbrs
        for node in all_area_nbrs:
            ter = [node.area, node.neighbour]
            area_index = parishes.index(node.area)
            address_id = address_ids[area_index]
            # add areas
            if self.AREAS.get(ter[0], None) is None:
                self.AREAS[ter[0]] = { "id":address_id, "trucks":[], "available_space":0 }
                
            # add neighbours
            nbring = (None, (ter[0], ter[1]))
            if nbring not in self.NBRS:
                self.NBRS.append(nbring)
                
        # get the Trucks, and Delivery for those booked areas
        booked_trucks = db.session.query(Truck).filter(
            (Truck.id.in_(truck_ids))
        ).all()
        
        # add booked Trucks to their respective areas
        for truck in booked_trucks:
            index = truck_ids.index(truck.id)
            parish = parishes[index]
            address_id = address_ids[index]
            
            if self.AREAS.get(parish, None) is not None: 
                if truck not in self.AREAS[parish]['trucks']:
                    self.AREAS[parish]['trucks'].append(truck) # add truck to list of trucks for this area
                    self.AREAS[parish]['available_space'] += truck.available # update the total available space of total truck booked for this area
            else: 
                self.AREAS[parish] = { "id":address_id, "trucks":[truck], "available_space":truck.available }
        
        if self.last:
            self.set_available_trucks(truck_ids)            
        
    def set_available_trucks(self, truck_ids):
        self.available_trucks = db.session.query(Truck).filter(~Truck.id.in_(tuple(truck_ids))).filter((Truck.active==1) & (Truck.available>0)).all()
        
    def discover( self, location ):
        """Discovers Areas by adding them to the areas PQ and updating the discovered dictionary with updated details.

        Args:
            ele (str): area name
        """ 
        area_depth = self.DEPTH.get(location, 1)
        if area_depth <= self.DEPTH['max_depth']:
            # check if area isn't already visited
            if location not in self.visited:
                next_depth = self.DEPTH[location] + 1
                available = self.AREAS[location]['available_space']
                
                # Add the current area to the PQ, if it isn't already in the PQ and Discovered Queue
                area = self.discovered.get(location, self.INF)
                if area is self.INF:
                    self.discovered[location] = available
                
                self.areas_in_depth.append(location)
                
                # check if max_depth reached, if not - get neighbours
                if area_depth < self.DEPTH['max_depth']:
                    
                    # discover neighbour and add them to PQ
                    nbrs = self.neighbours( location )
                    
                    for nbr in nbrs:
                        # set depth for the neighbours
                        if next_depth < self.DEPTH.get(nbr, self.INF) or self.DEPTH[nbr] is None: 
                            self.DEPTH[nbr] = next_depth
                        wt = self.AREAS.get( nbr, self.INF )
                        
                        if wt is not self.INF:
                            # Get total weight (wt) from area to each neighbour
                            nbr_sum = available + wt
                        
                            self.booked_areas.put((nbr_sum, nbr))
                            
                            # if value from area to a nbr is less than what is already in discovered, and neighbour not yet visited
                            if nbr_sum < self.discovered[nbr] and nbr not in self.visited:
                                                            
                                # updates nbr node in discovered, and add them to PQ
                                self.discovered[nbr] = nbr_sum
                                # trcks space less than the order quantity for each area in Priority Queue
                                self.areas_in_depth.append(nbr)
                            self.discover(nbr)
                    
                        
    
    def get_booked_areas(self):
        """
            Returns:
                Adjacency Matrix of all nodes as list of tuples
        """
        matrix = self.adjacency_list.items()
        return matrix

            
    def neighbours(self, area):
        
        """Provides a list of all the neighbours of a given area.

        Args:
            character (nbr): The name of the area that you want to find the neighbours of

        Returns:
            list: All the neighbours of the area
        """
        all_nbrs = []
        # initialize empty list of neighbours
        for nbrs in self.NBRS:
            nbr_list = list( map( str.casefold, nbrs[1] ) )
            if area.casefold() in nbr_list: 
                ind = (0, 1) [ nbr_list.index(area.casefold()) == 0 ]
                # gets the neighbour index
                nbr = nbrs[1][ind]
                # gets the neighbour node
                if nbr != None:
                    all_nbrs.append(nbr)
                    # adds the neighbour to the neighbours list
        return all_nbrs
    
    def update_db(self, order, address, qty, truck):
        try:
            # book truck/ fill truck
            truck = db.session.query(Truck).filter_by(id=truck.id).first()
            if qty >= truck.available and qty!=0 and truck.available > 0:
                # update qty
                qty -= truck.available
                truck.available = 0
                truck.active = 1
                # fill compartments
                comps = db.session.query(Compartments).filter_by(id=truck.id).all()
                # update compartments
                for comp in comps:
                    comp.order_id=order.id
                    comp.petrol = self.petrol
                # update delivery table
                delivery = Delivery(order.id, truck.id, address.id)
                db.session.add(delivery)
                # push updates and add delivery
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return qty
    
    def get_deliveries(self):
        return db.session.query(Delivery.parish, Delivery.truck_id, Delivery.address_id).distinct().join(Order, Order.id==Delivery.order_id).filter((Delivery.date==self.delivery_date) & (Order.delivery_time==self.delivery_time)).all()

        
    def fill_trucks(self, order, qty, address):
                
        deliveries = self.get_deliveries()
        truck_ids = [x[1] for x in deliveries]
        
        self.set_available_trucks(truck_ids)
        
        av_pq = PriorityQueue()
        # excess_comps = []
        for t in self.available_trucks:
            av_pq.put((-t.available, t))                
                
        if qty > 0:
            while not av_pq.empty():
                # go through the list of available trucks from largest to smallest
                this_truck = av_pq.get()[1]
                # the first truck to satisfy fill_order.QTY >= truck.available then fill it
                if qty >= this_truck.available:
                    qty = self.update_db(order, address, qty, this_truck)
                else:
                    break
                     
            # fill the order balance (qty) using the available booked trucks
            # if no available truck meets criteria then go through the booked trucks for available space 
            result = list(self.find_best_fit(order, qty, address))
            if result[0] == 0:
                return result[0], []
            
            # if still no space is found, go through the compartments of the available trucks to best fill the order by occupying cominations of a single truck's compartments
            if len(self.available_trucks):
                # fill each
                prev_qty = qty
                added = False
                
                for truck in self.available_trucks:
                    
                    try:
                        
                        # fill compartments
                        comps = db.session.query(Compartments, Truck)\
                        .filter(\
                            (Truck.id==Compartments.truck_id)\
                            & (Compartments.truck_id==truck.id)\
                            & (Compartments.order_id==0)\
                            & (Truck.active==1)).order_by(desc(Compartments.capacity)).all()
                        
                        # fill/update compartment from largest to smallest
                        for comp in comps:
                            if comp.Compartments.capacity <= qty:
                                prev_qty = qty
                                truck = comp.Truck
                                comp.Compartments.order_id=order.id
                                comp.Compartments.petrol = self.petrol
                                # book truck/ fill truck
                                comp.Truck.active = 1
                                comp.Truck.available -= comp.Compartments.capacity
                                
                                # update the database (truck.available)
                                db.session.add_all(comp)
                                
                                # update the qty
                                qty -= comp.Compartments.capacity
                                result[0] = qty
                                
                                db.session.commit()
                                
                            else:
                                # update upgrade suggestions queue
                                enqued = (abs(qty-comp.Truck.available), comp.Truck)
                                result[1].put(enqued)
                                
                        # update delivery table
                        delivery = Delivery(order.id, truck.id, address.id)
                        db.session.add(delivery)
                        db.session.commit()
                        added = True
                        
                    except Exception as e:
                        print(e)
                        db.session.rollback()
                        qty = prev_qty
                        if added:
                            db.session.delete(delivery)
                            db.session.delete(comp.Truck)
                            db.session.delete(comp.Compartments)
                            db.session.commit()
                
        truck_comps = []
        if not result[1].empty():
            truck = result[1].get()[1]
            truck_comps = db.session.query(Compartments.capacity).filter_by(truck_id=truck.id).filter_by(order_id=0).all()
        # store truck in global variable on server
        # lock truck in server for update
        return result[0], [x[0] for x in truck_comps]
        
    
    def find_best_fit( self, order, qty, address ):
        """Routine to discover and visit nodes in search for next best fit truck

        Args:
            depth (_type_): _description_
            qty (_type_): _description_
            location (_type_): _description_
        """
        trucks_pq = PriorityQueue() # automatically fill order using this queue
        trucks_pq_excess = PriorityQueue() # provide upgrade options using this queue
        self.discover( address.parish )
        
        # add trucks from this area to the priority queues
        area_trucks = self.AREAS[address.parish]['trucks']
        for truck in area_trucks:
            truck_pri = abs(qty - truck.available)
            if truck.available > 0:
                if qty >= truck.available: 
                    trucks_pq.put((truck_pri, truck))
                else: 
                    trucks_pq_excess.put((truck_pri, truck))
                
        # mark this area as visited
        self.visited.append(address.parish)
        
        # go through all the other areas (in the areas_in_depth list)
        for nbr in self.areas_in_depth:
                        
            if nbr is not None:
                
                # visit neighbour
                self.visited.append(nbr)
                
                # add trucks from this neighbouring area to the priority queues
                nbr_trucks = self.AREAS[nbr]['trucks']
                for truck in nbr_trucks:
                    truck_pri = abs(qty - truck.available)
                    if truck.available > 0:
                        if qty >= truck.available: 
                            trucks_pq.put((truck_pri, truck))
                        else: 
                            trucks_pq_excess.put((truck_pri, truck))
        
        # go through the trucks_pq to get the best fit while  
        while not trucks_pq.empty():
            diff, truck = trucks_pq.get()
            if diff >= 0:
                if qty >= diff:
                    qty = self.update_db(order, address, qty, truck)
                if qty == 0: break
        
        # return best fit upgrade recommendation queues                                
        return qty, trucks_pq_excess
            
    def get_nbr_element(self, ele, nbr ):
        """Provides a list with the wieght, start area and end area, if a neighbour relationship exists between the nodes

        Args:
            ele (str): area node;
            nbr (str): area node

        Returns:
            list: [weight, start_node, end_node] | None
        """
        ele_min = ele.casefold()
        nbr_min = nbr.casefold()
        for nbrs in self.NBRS:
            edge = list(map(str.casefold,nbrs[1]))
            if ele_min in edge and nbr_min in edge:
                src = (0, 1) [edge.index(ele_min) == 0]
                dst = 1-src
                return [nbrs[0], nbrs[1][src], nbrs[1][dst]]
        return [self.INF, ele, nbr]
    
if __name__=="__main__":
    g = Graph("F")
    print("ADJACENCY MATRIX:\n")
    for row in g.get_booked_areas():
        print(list(row))
    
    for i in range(2): 
        print()
    print("NODES VISITED:\n")
    print(g.visited)
