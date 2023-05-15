# Author: Marlon Lewis
# ID: 620001669

from queue import PriorityQueue
from app import db
from app.models import Order, Area, Truck, Address, Delivery, Compartments
from datetime import datetime
from app.utils.utils import format_date, sql_date, strtodate

class Graph:
    # Class for Building Graph's Adjacency Matrix
    available_trucks = []
    INF = float("Inf")

    def __init__(self, start_node, ord_qty, date, depth, last=False):
        """Graph Constructor
        """
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
        self.pq = list()
        self.excess = list()
        self.delivery_date = date
        self.load_area_nodes()
        locations = list(self.AREAS.keys())
        
        # get the booked areas (based on orders made) and initialize them
        for area in locations:
            # initialize discovered, adjacency matrix, distance matrix and other properties
            self.discovered[area] = [self.INF, None, self.AREAS[area]]
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
        self.pq = list()
        self.excess = list()
        
    def load_area_nodes(self):
        """Load up the graph data structure - contains areas and the trucks booked for each area"""
        date = sql_date(strtodate(self.delivery_date))   
        
        # get all deliveries scheduled for this delivery date     
        deliveries = db.session.query(Delivery.parish, Delivery.truck_id, Delivery.address_id).distinct().filter_by(date=self.delivery_date).all()
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
            self.available_trucks = db.session.query(Truck).filter(~Truck.id.in_(tuple(truck_ids))).filter_by(active=0).all()            
        
        
    def discover( self, location ):
        """Discovers Areas by adding them to the areas PQ and updating the discovered dictionary with updated details.

        Args:
            ele (str): area name
        """ 
        area = location.casefold()
        area_depth = self.DEPTH.get(area, 1)
        if area_depth <= self.DEPTH['max_depth']:
            # check if area isn't already visited
            if area not in self.visited:
                next_depth = self.DEPTH[area] + 1
                available = self.AREAS[area]['available_space']
                
                # Add the current area to the PQ, if it isn't already in the PQ and Discovered Queue
                if self.discovered.get(area, None) is None:
                    area_space = [None, area]
                    self.pq.append(area_space)
                    self.discovered[area] = [available, None, area]
                
                # check if max_depth reached, if not - get neighbours
                if area_depth < self.DEPTH['max_depth']:
                    
                    # discover neighbour and add them to PQ
                    nbrs = self.neighbours( area )
                    for nbr in nbrs:
                        # set depth for the neighbours
                        if next_depth < self.DEPTH[nbr] or self.DEPTH[nbr] is None: self.DEPTH[nbr] = next_depth
                        wt = self.get_nbr_element( area, nbr )[0]
                        
                        # Get total weight (wt) from area to each neighbour
                        nbr_sum = available + wt
                        
                        self.booked_areas.put((nbr_sum, nbr))
                        
                        # if value from area to a nbr is less than what is already in discovered, and neighbour not yet visited
                        if nbr_sum < self.discovered[nbr][0] and nbr not in self.visited:
                                                        
                            # updates nbr node in discovered, and add them to PQ
                            self.discovered[nbr] = [nbr_sum, area, nbr] 
                            # trcks space less than the order quantity for each area in Priority Queue
                            self.pq.append([area, nbr])
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
    
    def fill_trucks(self, order, qty, address):
        trucks_pq = PriorityQueue()
        trucks_pq_excess = PriorityQueue()
        self.discover( address.parish )
        # filled_trucks = []
        
        # fill trucks
                
        deliveries = db.session.query(Delivery.parish, Delivery.truck_id, Delivery.address_id).distinct().filter_by(date=self.delivery_date).all()
        truck_ids = [x[1] for x in deliveries]
        
        self.available_trucks = db.session.query(Truck).filter(~Truck.id.in_(tuple(truck_ids))).filter_by(active=0).all()
        
        temp = []
        av_pq = PriorityQueue()
        for t in self.available_trucks:
            av_pq.put((-t.available, t))                
                
        if qty >= 0:
            while not av_pq.empty():
                # go through the list of available trucks from largest to smallest
                this_truck = av_pq.get()
                # the first truck to satisfy fill_order.QTY >= truck.available then fill it
                if qty >= this_truck.available:
                    # update qty
                    qty -= this_truck.available
                    # book truck/ fill truck
                    this_truck.available = 0
                    db.session.add(this_truck)
                    # fill compartments
                    comps = db.session.query(Truck).filter_by(id=this_truck.id).all()
                    for comp in comps:
                        comp.order_id=order.id
                        db.session.add(comp)
                    # update delivery table
                    delivery = Delivery(order.id, this_truck.id, address.id)
                    db.session.add(delivery)
                else:
                    break
                     
            # fill the order balance (qty) using the available booked trucks
            # if no available truck meets criteria then go through the booked trucks for available space 
            
            # if still no space is found, go through the compartments of the available trucks to best fill the order by occupying cominations of a single truck's compartments
            pass
                
                
                truck_pri = qty - truck.available_space
                trucks_pq.put((truck_pri, truck))
            else: 
                truck_pri = truck.available_space - qty
                trucks_pq_excess.put((truck_pri, truck))
                
        # mark this area as visited
        self.visited.append(area)
        yield qty
    
    def find_best_fit( self, order, qty, address ):
        """Routine to discover and visit nodes in search for next best fit truck

        Args:
            depth (_type_): _description_
            qty (_type_): _description_
            location (_type_): _description_
        """
        trucks_pq = PriorityQueue()
        trucks_pq_excess = PriorityQueue()
        self.discover( address.parish )
        
        # add trucks from this area to the priority queues
        area_trucks = self.AREAS[area]['trucks']
        for truck in area_trucks:
            if self.QTY >= truck.available: 
                truck_pri = self.QTY - truck.available_space
                trucks_pq.put((truck_pri, truck))
            else: 
                truck_pri = truck.available_space - self.QTY
                trucks_pq_excess.put((truck_pri, truck))
                
        # mark this area as visited
        self.visited.append(area)
        
        # go through all the areas in the pq
        for _, nbr in self.pq:
                        
            if nbr is not None:
                
                # visit neighbour
                self.visited.append(nbr)
                
                # add trucks from this neighbouring area to the priority queues
                nbr_trucks = self.AREAS[nbr]['trucks']
                for truck in nbr_trucks:
                    if self.QTY >= truck.available_space: 
                        truck_pri = self.QTY - truck.available_space
                        trucks_pq.put((truck_pri, truck))
                    else: 
                        truck_pri = truck.available_space - self.QTY
                        trucks_pq_excess.put((truck_pri, truck))
        # return priority queues to use in best fit                           
        return trucks_pq, trucks_pq_excess
            
    def get_nbr_element(self, ele, nbr ):
        """Provides a list with the wieght, start area and end area, if a neighbour relationship exists between the nodes

        Args:
            ele (str): area node;
            nbr (str): area node

        Returns:
            list: [weight, start_node, end_node] | None
        """
        for nbrs in self.NBRS:
            edge = list(map(str.casefold,nbrs[1]))
            if ele.casefold() in edge and nbr.casefold() in edge:
                src = (0, 1) [edge.index(ele) == 0]
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
