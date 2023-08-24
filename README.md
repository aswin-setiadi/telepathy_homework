# README

## Setup (Tested on Windows 10 Python 3.10.6)

- Checkout master branch
- In root folder, run ```$pip install -r req-dev.txt```


## Question 1-1

### Assumptions

- Odd floor A -> E
- Even floor E -> A
- Guest x+1 can checkout earlier than guest x
- There are maximum of 5 rooms in each floor
- When there is no available room to assign, application will return None


### How to Run

- To play with the application, change question1-1.py as needed and run with ```$python question1-1.py```

## Question 1-2

### Discussion

We first loop and visit each room and find/ track number of rooms to be infected and number of healthy guests at this unit of time. If infection is spreading, update the map status and loop to the next unit of time. If not, check if healthy guests exist, if yes, it means they are unreachable by the infected guest, so return **-1**. Else, return the number of current **unit_time**.

Each room should be visited only once (helped and tracked by **visited_matrix**), so the runtime should be ~ d x c x M x N where d is time for virus to converge infecting everyone, c is a constant, M is number of row, N is number of column. In worst case scenario when all room is uninfected except 1 infected room, d will not reach M x N runs since the virus spread in 2-4 direction in 1 unit of time.

### Algorithm

1. Start with for loop of time with **unit_time**=0. 
2. Loop 1 room at a time starting at row 0 col 0.
    - If visit is marked **to_be_infected** and room is 1, add room to **rooms_to_infect** list if it has not been added.
    - If room is visited before, continue, else update **visited_matrix**. 
    - If room is 0, go to next room
    - If room is 1, update **healthy_guests** list if it is not there.
    - If room is 2, find the room neighbours, for each neighbour repeat the above.
3. After room loops ends, if **to_be_infected** list is empty:
    - If **healthy_guests** list is empty return **unit_time**
    - Else return -1
8. Else update hotel matrix following **rooms_to_infect** list, reset the list, add **unit_time** by 1, and continue to next **unit_time** loop. 

### How to Run

- To play with the application, change question1-2.py as needed and run with ```$python question1-2.py```

## Question 2

### Files

Open question2.png for both 1st and 2nd graph or use https://app.diagrams.net/ and load question2.drawio.

### Discussion

In the 1st graph, grouping each entity or node is very difficult as we need to scan each node and find those with the same brand. It is also difficult to differentiate between cars or tires as they are implied through their relationship. 

In the 2nd graph, it is easier to group a set/ subset of an object type as they are labeled according to their object type instead of object name. From this, we can also quickly deduce what kind of object the entity is.

The advantage of graph based database is that when joining entities, it is much faster then the typical relational database join, as they are using index-free adjancency processing whereby each connected nodes are pointed to each other, so it is just using a memory pointer lookup.

Few query use cases:

1. Find all Toyota cars.
    - The database will get **CarProducer** with name: Toyota.
    - Then it will search **Car** that it produce.

2. Find all the Michelin tires that have optimal durability to Toyota Supra.
    - The database will find **TireProducer** with name: Michelin and retrieved all it's **Tire**, alias as **t**
    - Then find **Car** that is produced by **CarProducer** with name: Toyota, filter by car name: Supra, alias **c**
    - filter **t** according to **can_be_fixed_on** with durability: optimal towards **c**

One downside of graph database is that if 2 entities relationship is not define, it may not scale well in large dataset. For example, if we want to find all tires that can not be fixed on Toyota Supra, the database will have to scan all the tires that has no **can_be_fixed_on** relatioship to **Car** with name Supra. Therefore, proper use case ideation and schema planning (despite being schema-less database) of the graph is warranted.
