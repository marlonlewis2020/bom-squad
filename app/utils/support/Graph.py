# Author: Marlon Lewis
# ID: 620001669

from queue import PriorityQueue
from ....app import db
from ....app.models import Order, Area, Truck

class Graph:
    # Class for Building Graph's Adjacency Matrix
    
    AREAS = {} # Area Data and Trucks
    """{"Kingston": { "id":1, "node":{}, "trucks":[], "available_space":0 }, 
        "St. Catherine": { "id":2, "node":{}, "trucks":[], "available_space":60 }, 
        "Clarendon": { "id":3, "node":{}, "trucks":[], "available_space":10 }, ...}"""
    QTY = 0
    DEPTH = {}
    INF = float("Inf")
    NBRS = [] # Edges depicting space available
    """[ (0, (None, "Kingston")), (1, ("Kingston", "St. Catherine")), (1, ("Kingston", "Clarendon")),
        (1, ("St.Catherine", "Clarendon")), (3, ("St. Catherine", "Manchester")), ... ]"""
    
    # (weight, ())

    discovered = {}
    adjacency_list = {}
    booked_areas = PriorityQueue()

    def __init__(self, start_node, ord_qty, depth):
        """Graph Constructor
        """
        self.QTY = ord_qty
        self.DEPTH['max_depth'] = depth
        self.DEPTH[start_node] = 1
        self.load_area_nodes()
        self.start_node = start_node
        self.visited = []
        self.pq = list()
        self.excess = list()
        locations = self.AREAS.keys()
        
        for area in locations:
            # initialize discovered, adjacency matrix, distance matrix and other properties
            self.discovered[area] = [self.INF, None, self.AREAS[area]]
            self.adjacency_list[area] = []
        
        for area in locations:
            nbrs = self.neighbours(self.AREAS[area])
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
        all_nodes = db.session.query(Area).filter_by().all() # filter by field that states if the area has any trucks assigned
        for node in all_nodes:
            area_location = node.location # get field that identifies the location
            area_trucks = db.session.query(Truck).filter_by(location=area_location).all() # filter by field that identifies the area
            self.AREAS[area_location] = { "id":node.id, "node":node, "trucks":area_trucks, "available_space":node.available_space }
            for nbr in self.neighbours(area_location):
                self.NBRS.append((nbr.space, (area_location, nbr)))
                
        
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
            if area.casefold() in list( map( str.casefold, nbrs[1] ) ): 
                ind = (0, 1) [ nbrs[1].index(area.casefold()) == 0 ]
                # gets the neighbour index
                nbr = nbrs[1][ind]
                # gets the neighbour node
                if nbr != None:
                    all_nbrs.append(nbr)
                    # adds the neighbour to the neighbours list
        return all_nbrs
    
    
    def find_best_fit( self, area ):
        """Routine to discover and visit nodes in search for next best fit truck

        Args:
            depth (_type_): _description_
            qty (_type_): _description_
            location (_type_): _description_
        """
        trucks_pq = PriorityQueue()
        trucks_pq_excess = PriorityQueue()
        self.discover( area )
        
        # add trucks from this area to the priority queues
        area_trucks = self.AREAS[area]['trucks']
        for truck in area_trucks:
            if self.QTY >= truck.available_space: 
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
