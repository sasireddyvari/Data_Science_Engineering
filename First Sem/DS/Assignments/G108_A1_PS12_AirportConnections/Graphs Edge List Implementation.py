#!/usr/bin/env python
# coding: utf-8

# ### DSAD ASSIGNMENT - 1

# #### GROUP 108
# - Reddyvari Sasi Kumar
# - Mohd Saif Ali 
# - Dhruba Adhikary

# #### Problem Statement : 
# 
# The CEO of a leading airline company wants to know if his flights are servicing all major cities /airports such that if a passenger wants to travel from a given starting city, they can reach any of the other cities using either a direct flight (0 stops) or an indirect flight (multiple stops at intermediate cities).
# 
# If there are any cities that are not reachable, the CEO wants to know the minimum number of flights (one-way flights) that need to be added so that the passenger can reach any destination city from the starting city using either direct or indirect flights.
# 
# You are given a list of city airports (three-letter codes like “JFK”), a list of routes (one-way flights from one airport to another like [“JFK” , “SFO”] ), and a starting city / airport.
# 
# Note that routes only allow you to fly in one direction; for instance, the route [“JFK”, “SFO”] only allows you to fly from “JFK” to “SFO” and not from SFO to JFK.
# 
# Also note that the connections don’t have to be direct (take off at the starting airport and land in the destination airport). It is okay if the destination airport can be reached from the starting airport by stopping at other intermediary airports in between.

# In[1]:


# !python -V

# Python 3.7


# In[2]:


def compute_flights(airports,routes,starting_airport):
# dealing with data error cases
    if len(starting_airport) == 0:
        return print("Starting Airport is not given")
    if len(airports) == 0:
        return "Airports list is empty"
# creating graph to store airports and routes list
    data_graph = compute_graph(airports,routes)
# finding unreachable airports with our given airports
    unreachable_airports = compute_unreachable(data_graph,airports,starting_airport)
# computing score of number of unreachable airports that can be reached leveraging unreachable airport
    unreachable_score(data_graph,unreachable_airports)
    return compute_connects(data_graph,unreachable_airports,starting_airport)


# In[3]:


def compute_connects(data_graph,unreachable_airports,starting_airport):
    #sorting airports in accordance with score
    unreachable_airports.sort(key = lambda airport:(len(airport.unreachable_connections),airport.airport), reverse = True)
    reaching_newconnections = []
    new_connections = 0
    for aiport_node in unreachable_airports:
        if aiport_node.is_reachable:
            continue
        new_connections = new_connections+1
        reaching_newconnections.append([starting_airport,aiport_node.airport])
        for connection in aiport_node.unreachable_connections:
            data_graph[connection].is_reachable = True
    return (new_connections, reaching_newconnections)


# In[4]:


def compute_graph(airports, routes):
    data_graph = {}
    for airport in airports:
        data_graph[airport] = AirportNode(airport)
    for route in routes:
        airport, connection = route
        data_graph[airport].connections.append(connection) # We gonna add the connection in the parent
    return data_graph


# In[5]:


def compute_unreachable(data_graph, aiports, starting_airport):
    visited_aiports = {}
    compute_depth_first_search(data_graph, starting_airport, visited_aiports)
    unreachable_airports = []
    for airport in aiports:
        if airport in visited_aiports:
            continue 
        else:
            air_node = data_graph[airport]
            air_node.is_reachable = False
            unreachable_airports.append(air_node)
    return unreachable_airports


# In[6]:


def compute_depth_first_search(data_graph, airports, visited_aiports):
    if airports in visited_aiports:
        return
    visited_aiports[airports] = True 
    connections = data_graph[airports].connections
    for connection in connections:
        compute_depth_first_search(data_graph, connection, visited_aiports)


# In[7]:


def unreachable_score(data_graph, unreachable_airports):
    for aiport_node in unreachable_airports:
        airpt = aiport_node.airport
        unreachable_connections = []
        depth_first_append(data_graph, airpt, unreachable_connections, {})
        aiport_node.unreachable_connections = unreachable_connections


# In[8]:


def depth_first_append(data_graph, airport, unreachable_connections, visted_airports):
    if data_graph[airport].is_reachable:
        return 
    if airport in visted_airports:
        return
    visted_airports[airport] = True 
    unreachable_connections.append(airport) 
    connections = data_graph[airport].connections
    for connection in connections:
        depth_first_append(data_graph, connection, unreachable_connections, visted_airports)


# In[9]:


class AirportNode:
    def __init__(self,airport):
        self.airport = airport
        self.connections = []
        self.is_reachable = True
        self.unreachable_connections = []


# ## Reading the Input File

# In[10]:


f = open('inputsPS12.txt', 'r')
lines = f.readlines()
f.close()


# In[11]:


data = ' '.join([line.strip() for line in lines])
# print(data)
keywords = ['airports','routes','Starting Airport']
idx = []
for index in keywords:
  idx.append(data.index(index))
idx.append(len(data))
# print(idx)


# In[12]:


airports_idx = data[idx[0]:idx[1]]
routes_idx = data[idx[1]:idx[2]]
starting_airport_idx = data[idx[2]:]
# print(airports_idx)

#----------------------Airports-----------------------------
airports = []
unstructured_airports = (airports_idx.split()[2:])
for airport in unstructured_airports:
  airports.append(airport[:3])
# print(airports)
# len(airports)

#---------------------Routes--------------------------------
unstructured_routes = routes_idx.split()[1:]
routes = []
for route in unstructured_routes:
  routes.append(route[:3])
group = []
route_pairs = []
index = 0
for index,route in enumerate(routes):
    group.append(route)
#     print(group)
    if((index+1)%2 == 0):
        route_pairs.append(group) 
        group = []
#         print(route_pairs)
# print(routes)
# print(route_pairs)
# len(routes)

#---------------------Starting Airport----------------------
starting_airport = []
starting_airport = starting_airport_idx.split()[-1:]
starting_airport = ''.join(starting_airport)
# print(starting_airport)
# len(starting_airport)


# ## Output File

# In[13]:


import sys as s
initial_stdout = s.stdout
s.stdout = open("outputPS12.txt", "w")
ans = compute_flights(airports, route_pairs,starting_airport)
print("The minimum flights that need to be added:",ans[0])
print("The flights that need to be added are:",ans[1])
s.stdout.close()
s.stdout = initial_stdout


# In[ ]:




