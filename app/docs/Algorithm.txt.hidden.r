
order <- order details
area_list <- List
best_fit_pq <- PriorityQueue
upgrade_pq <- PriorityQueue
dpt <- get max depth
g <- initialize the graph
data <- get all data from database
areas <- initialize area of areas
x <- get delivery area from order
x_d <- initialize the depth of x to 1
b <- get order balance
neighbourhood <- initialize empty dictionary


// GREEDILY FILL UNBOOKED TRUCKS
unbooked <- get all unbooked trucks
unbooked <- sort unbooked trucks by capacity DESC
Loop over unbooked trucks as b:
    if order balance b >= capacity of truck
        fill truck
        remove truck from unbooked
        b <- b-capacity of truck
    else:
        END LOOP


// BUILD GRAPH OF BOOKED TRUCKS IN EACH AREA
loop over areas as area up tp depth dpt
    loop over all booked trucks as truck in the area
        pri <- abs(b-available)
        if b >= available space in truck:
            best_fit_pq <- add truck with pri
            b <- pri
        else:
            upgrade_pq <- add truck with pri

    nbrs <- find neighbours

    loop over nbrs as nbr up to depth dpt
        if nbr not yet discovered:
            set depth of nbr to INF
            areas <- add nbrs to graph
            relationship <- set depth of nbr to depth of area + 1
            loop over all booked trucks as truck in the nbr
                pri <- abs(b-available)
                if b >= available space in truck:
                    best_fit_pq <- add truck with pri
                    b <- pri
                else:
                    upgrade_pq <- add truck with pri
    neighbourhood <- store the neighbours of each area


// VISIT TRUCK NODES IN PQ TO GET BEST FIT
Loop until best_fit_pq is empty:
    truck <- pop truck from best_fit_pq
    if order balance b < truck space available:
        END LOOP
    else:
        fill truck
        b <- b-truck space available

if order is not filled:
    truck <- pop truck from upgrade_pq

// Partially Fill unbooked trucks
Add remaining booked trucks to unbooked pq
Loop over remaining unbooked trucks as truck
    pri <- abs(b-truck capacity)
    unbooked_pq <- add truck with pri

Loop while order balance b > 0:
    truck <- pop truck from unbooked_pq
    get compartments of truck
    sort compartments by capacity DESC
    while order balance b >= capacity of compartment
        fill compartments until
        b <- b-capacity of ompartment

if order balance b != 0:
    suggestion = upgrade_pq.pop()
    comps <- get capacity of all compartments as list
else:
    comps = []

return b, comps