import math



class BinaryHeap:
    NIL = 0
    last_inserted_index = 1
    root_index = 2
    
    def __init__(self):
        # sets initial to the number of data inserted in structure to 0
        # sets initial scaling factor to increase by to 2
        # sets initial empty cell vlaues to NIL to be later updated
        self.v = [0,2,(self.NIL)]
        # FYI, example data structure with one node inserted: [1, 3, el, NIL, NIL]

    # PREDICATES
    
    def in_list(self, index_pos):
        return index_pos <= self.last_inserted_index and index_pos >= 2
    
    def order_violated(self, child, parent):
        '''
            MAX HEAP CHECK/CORRECTION CRITERIA: child > parent
            MIN HEAP CHECK/CORRECTION CRITERIA: child < parent
        '''
        return self.get_pri(child) < self.get_pri(parent)
    
    def get_pri(self, el):
        return el[0]
    
    # ACCESSORS
    
    def size(self):
        return self.v[0]
    
    def parent(self, n):
        return math.ceil(n/2)

    def left(self, n):
        return 2*n - 1

    def right(self, n):
        return 2*n

    # MUTATORS
    
    def swap(self, pos_i, pos_j):
        self.v[pos_j], self.v[pos_i] = self.v[pos_i], self.v[pos_j]

    def heap_insert(self, el):
        posn = self.last_inserted_index + 1
        if posn >= len(self.v):
            self.nexy_array()
        self.v[posn] = el
        self.v[0] = self.last_inserted_index
        self.v[1] += 1
        self.last_inserted_index += 1
        self.bubble_up(posn)
    
    def pop(self):
        # pop/get the root node
        node = self.v[self.root_index]
        if self.size()>0:
            # copy the last node to the root
            self.v[self.root_index] = self.v[self.last_inserted_index]
            # replace/set the original position of the copied node with NIL
            self.v[self.last_inserted_index] = self.NIL
            # update the index for the last inserted node
            self.v[0] -= 1
            self.last_inserted_index -= 1
            # initiate the bubble_down method to organize the heap in order
            self.bubble_down(self.root_index) 
            # return the popped node
        return node
    
    # SUPPORT
    
    def bubble_up(self, next_insert_index_posn):
        if next_insert_index_posn > 2:
            parent_posn = self.parent(next_insert_index_posn)
            value = self.v[next_insert_index_posn]
            parent_value = self.v[parent_posn]
            if self.order_violated(value, parent_value):
                self.swap(next_insert_index_posn, parent_posn)
                self.bubble_up(parent_posn)
                
    def bubble_down(self, parent_index):
        left_index = self.left(parent_index)
        right_index = self.right(parent_index)
        if self.in_list(left_index) and self.in_list(right_index):
            choice = self.get_smaller_node(right_index,left_index) # returns the index of the smaller node
            if self.order_violated(self.v[choice], self.v[parent_index]):
                self.swap(choice,parent_index)
                self.bubble_down(choice)
        elif self.in_list(left_index):
            if self.order_violated(self.v[left_index], self.v[parent_index]):
                self.swap(left_index,parent_index)
                self.bubble_down(left_index)
        elif self.in_list(right_index) and self.order_violated(self.v[right_index], self.v[parent_index]):
            self.swap(right_index,parent_index)
            self.bubble_down(right_index)
    
    def get_smaller_node(self, left, right):
        return (right,left)[self.get_pri(self.v[left]) < self.get_pri(self.v[right])]
    
    def nexy_array(self):
        # creates a new array larger than the current array
        s_factor = self.v[1]
        size = len(self.v) + s_factor
        # The next array's size is the lenght of current + scaling factor
        new_array = [self.NIL]*size
        for cell in range(self.last_inserted_index+1):
            new_array[cell] = self.v[cell]
            # populates the next array with all the current array's values
        self.v = new_array