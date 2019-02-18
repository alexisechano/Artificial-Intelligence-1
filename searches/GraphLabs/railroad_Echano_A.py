# Name: Alexis Echano        Data: 10/31/18
import heapq, random, pickle, math, time
from collections import deque
from math import pi, acos, sin, cos


class PriorityQueue():
    """Implementation of a priority queue
    to store nodes during search."""

    # TODO 1 : finish this class


    def __init__(self): #initializes the PQ object
        self.queue = []
        self.current = 0

    def next(self): #goes to next node in queue
        if self.current >= len(self.queue):
            self.current
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def pop(self):  #pops the highest priority
        node = heapq.heappop(self.queue)
        return node     #returns popped value

    def remove(self, nodeId):   #removes at certain value
        item = self.queue.remove(nodeId)
        return item  # returns popped value

    def __iter__(self):
        return self

    def __str__(self):
        return 'PQ:[%s]' % (', '.join([str(i) for i in self.queue]))

    def append(self, node):
        heapq.heappush(self.queue, node)

    def __contains__(self, key):
        self.current = 0
        return key in [n for v, n in self.queue]

    def __eq__(self, other):
        return self == other

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue = []

    def top(self):
        return self.queue[0]

    __next__ = next

'''Making class Graph(), Node(), and Edge() are optional'''
'''You can make any helper methods'''


def make_graph(nodes_file, node_city_file, edge_file):  # graph will be a list of nodes
    nodes = open(nodes_file, 'r')
    edges = open(edge_file, 'r')
    names = open(node_city_file, 'r')

    edge_dict = {}
    name_dict = {}

    graph_dict = {}  # the graph: key is node number while value is the Node object

    for edge in edges.readlines():
        line_edge = edge.split()    #number, adj

        node_num = line_edge[0]
        adj = line_edge[1]

        if(node_num not in edge_dict.keys()):
            edge_dict[node_num] = [adj]
        if(adj not in edge_dict.keys()):
            edge_dict[adj] = [node_num]

        if(node_num in edge_dict.keys()):
            edge_dict[node_num].append(adj)
        if(adj in edge_dict.keys()):
            edge_dict[adj].append(node_num)

    for name in names.readlines():
        line_names = name.split(" ", 1)   #number, name

        node_number = line_names[0]
        node_name = line_names[1].strip("\n")

        name_dict[node_name] = node_number

    for node in nodes.readlines():  #goes through nodes text file with coordinates
        line_node = node.split() #   node num, long, lat

        num = line_node[0]   #   node number
        coordinates = (line_node[1], line_node[2])    #coordinates

        if(num not in graph_dict):
            new_node = [coordinates, edge_dict[num]]    #the node
            graph_dict[num] = new_node

    return [name_dict, graph_dict]  #list of dictionaries

def find_name(dict, id):
    for i in dict.keys():
        if(dict[i] == id):
            return i
    return -1

def calc_edge_cost(start, end, graph):
    # TODO: calculate the edge cost from start city to end city
    #       by using the great circle distance formula.
    #       Refer the distanceDemo.py

    s = graph[start]
    e = graph[end]


    y1 = float(s[0][1])
    x1 = float(s[0][0])
    y2 = float(e[0][1])
    x2 = float(e[0][0])

    #
    R = 3958.76  # miles = 6371 km

    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


def generate_path(current, explored, g, namedict, graph):# generates path from explored
    list = [current]    #adds current to list
    city_names = [] #initializes city names
    cost = 0    #cost is now 0
    while explored[current] != "":       #assume the parent of root is ""
        list.append(explored[current])
        cost += calc_edge_cost(current, explored[current], graph)   #adds to cost

        if(find_name(namedict, current) != -1):
            city_names.append(find_name(namedict, current)) #adds to city list
        current = explored[current]

    if (find_name(namedict, current) != -1):
        city_names.append(find_name(namedict, current))  # adds to city list if not already

    return [list[::-1], len(explored), cost, city_names[::-1]]  #returns values


def breadth_first_search(start, goal, graph):
    # TODO: finish this method
    #       print the number of explored nodes somewhere

    #   "base case"
    if start == goal: return []

    #   name dictionary
    name_dictionary = graph[0]

    #   graph actual
    graph_main = graph[1]   #   key is the id, value is the coordinates and adjacents

    #   sets the current state at the initial = has to be number
    current_state = name_dictionary[start]

    #   dictionary to store states in path
    explored = {current_state: ""}

    #   creates queue for frontier, holds strings of numbers only!!
    frontier = deque()

    #   sets current node: [coord, adjacents]
    current = graph_main[current_state]

    #   adds initial state to the PQ
    frontier.append(current_state)

    #   goal number
    goal_num = name_dictionary[goal]

    #   loop runs until the queue is empty or NO SOLUTION
    while(len(frontier) > 0):
        #   pops the PQ
        current_state = frontier.popleft()
        current = graph_main[current_state] # returns the node with the matching number as current_state

        if (current_state == goal_num):  #   checks goal state and prints out the path
            # returns the path of id, count of expanded nodes, cost, and city name path too
            return generate_path(current_state, explored, goal_num, name_dictionary, graph_main)
        else:
            #   for every newly generated child, it checks each new state if added to explored
            for a in current[1]:    #numbers!
                if(a not in explored):
                    frontier.append(a)
                    explored[a] = current_state     #   child: parent added to dictionary
    #   returns no solution
    return []


def dist_heuristic(v, goal, graph):
    #     # TODO: calculate the heuristic value from node v to the goal

    heur = 0
    x1, y1 = graph[v][0]
    x2, y2 = graph[goal][0]

    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)

    heur = abs(y2-y1) + abs(x2-x1)

    return heur

def a_star(start, goal, graph, heuristic=dist_heuristic):
    # TODO: Implement A* search algorithm
    #       print the number of explored nodes somewhere

    #   sets up the PQ as a frontier
    frontier = PriorityQueue()

    #   name dictionary
    name_dictionary = graph[0]

    #   graph actual
    graph_main = graph[1]

    #   goal id number
    goal_num = name_dictionary[goal]

    #   sets the current state at the initial = has to be id number
    current_state = name_dictionary[start]

    #   to generate the path
    parents = {current_state: ""}    #parents --> path

    #   explored set up with pathcosts
    explored = {current_state: 0}   #holds path costs + depth

    #   sets current node: [coord, adjacents]
    current = graph_main[current_state]

    #   if start is already equal to goal
    if start == goal: return []

    #   if not then run A* search
    else:
        cost = 0 + heuristic(current_state, goal_num, graph_main)   #calculates the g (which is 0) + h (generates heuristic)
        value = current_state
        frontier.append((cost, value, current))   #appends the node to the frontier (h, node that holds adjacents)

        while(frontier):   #while the frontier isn't empty
            current = frontier.pop()  #pops the priority value -> (h, node of coords and list)
            value = current[1]  #node id
            adjacents = current[2][1]   #access the adjacents

            # check if a path is found
            if(value  == goal_num):#accesses the node value using the tuple and checks if goal
                return generate_path(value, parents, goal_num, name_dictionary, graph_main) #returns the path

            for c in adjacents:    #goes through adjacent values
                g = explored[value] + 1   #calc g by value or current id

                if(c not in explored or g < explored[c]):
                    explored[c] = g  # adds to costs (depths) by node id
                    h = heuristic(c, goal_num, graph_main)  #calc h
                    f = explored[c] + h   # calculates f(n)
                    parents[c] = value    #adds to parents
                    frontier.append((f, c, graph_main[c]))  #adds to frontier,... a new node

   #if nothing is found, return none
    return []

def generate_path_bidirec(e_front, e_back, value, end, namedict, graph):
    #   creates new path for front side
    pathFront = [value]

    #   creates new path for back side
    pathBack = []

    #   sets a temp value
    curr = value

    #   cost initialization
    cost = 0

    #   creates new path for front side of city names
    city_names_front = []

    #   creates new path for back side of city names
    city_names_back = []

    #   generates path for the front explored
    while e_front[value] != "":       #goes until it hits start
        if (e_front[value] not in pathBack):
            pathFront.append(e_front[value])
            cost += calc_edge_cost(e_front[value], value, graph)
        #   appends to the path list and checks city names

        if(find_name(namedict, value) != -1 and value in pathFront):
            city_names_front.append(find_name(namedict, value))
        value = e_front[value]

    #   adds final city to front
    if (find_name(namedict, value) != -1 and value in pathFront):
        city_names_front.append(find_name(namedict, value))

    #   #   starts back at start value for cost
    start = value

    #   starts back at converging value
    value = curr

    #   generates path for the end explored
    while e_back[value] != "":  # until it hits end
        if(e_back[value] not in pathFront):
            pathBack.append(e_back[value])
            cost += calc_edge_cost(e_back[value], value, graph)
        #   appends to the path list and checks city names
        if (find_name(namedict, value) != -1 and value in pathBack):
            city_names_back.append(find_name(namedict, value))
        value = e_back[value]

    #   adds final city to back
    if (find_name(namedict, value) != -1 and value in pathBack):
        city_names_back.append(find_name(namedict, value))

    #    returns value
    return [pathFront[::-1] + pathBack, len(e_front) + len(e_back), cost, city_names_front[::-1] + city_names_back]

def bidirectional_BFS(start, goal, graph):
    # TODO: Implement bi-directional BFS
    #       print the number of explored nodes  somewhere

    #   "base case"
    if start == goal: return []

    #   name dictionary
    name_dictionary = graph[0]

    #   graph actual
    graph_main = graph[1]   #   key is the id, value is the coordinates and adjacents

    #   sets the current state at the initial = has to be number
    current_state = name_dictionary[start]

    #   dictionary to store states in path
    explored_start = {current_state: ""}

    #   creates queue for frontier starting from start, holds strings of numbers only!!
    frontier_start = deque()

    #   creates queue for frontier starting from back, holds strings of numbers only!!
    frontier_goal = deque()

    #   sets current node: [coord, adjacents]
    current = graph_main[current_state]

    #   adds initial state to the PQ
    frontier_start.append(current_state)

    #   goal number
    goal_num = name_dictionary[goal]

    #   dictionary to store states in path
    explored_back = {goal_num: ""}

    #   adds initial (goal state to the PQ
    frontier_goal.append(goal_num)

    #   loop runs until the queue is empty or NO SOLUTION
    while(frontier_start and frontier_goal):
        #   pops the PQs
        current_state_start = frontier_start.popleft()
        current_start = graph_main[current_state_start] # returns the node with the matching number as start side

        current_state_end = frontier_goal.popleft()
        current_end = graph_main[current_state_end] # returns the node with the matching number as end side

        if(current_end == current_state):
            #   if the two values are equal, return
            return generate_path_bidirec(explored_start, explored_back, current_state, goal_num, name_dictionary, graph_main)  # returns the path
        else:
            #   for every newly generated child, it checks each new state if added to explored
            for a in current_start[1]:    #numbers!
                if(a not in explored_start):
                    #   appends to the front
                    frontier_start.append(a)

                    explored_start[a] = current_state_start     #   child: parent added to dictionary
                #   checks intersection
                if (a in frontier_start and a in frontier_goal and a in explored_back):
                    return generate_path_bidirec(explored_start, explored_back, a, goal_num, name_dictionary, graph_main)  # returns the path

            for b in current_end[1]:    #numbers! (ids)
                if(b not in explored_back):
                    #   appends to the back
                    frontier_goal.append(b)
                    explored_back[b] = current_state_end     #   child: parent added to dictionary

                #   checks intersection
                if(b in frontier_start and b in frontier_goal and b in explored_start):
                    return generate_path_bidirec(explored_start, explored_back, b, goal_num, name_dictionary, graph_main)  # returns the path

    #   returns no solution
    return []


def bidirectional_a_star(start, goal, graph, heuristic=dist_heuristic):
    # TODO: Implement bi-directional A*
    #       print the number of explored nodes somewhere
    #       print the number of explored nodes somewhere

    #   sets up the PQ as a frontier
    frontier_start = PriorityQueue()

    #   sets up the PQ as a frontier
    frontier_goal = PriorityQueue()

    #   name dictionary
    name_dictionary = graph[0]

    #   graph actual
    graph_main = graph[1]

    #   checks if input is already an id
    if(not goal.isdigit()):
    #   goal id number
        goal_num = name_dictionary[goal]
    else:
        goal_num = goal

    #   checks if input is already an id
    if (not start.isdigit()):
    #   sets the current state at the initial = has to be id number
        current_state = name_dictionary[start]
    else:
        current_state = start

    #   sets current node: [coord, adjacents]
    front_current = graph_main[current_state]

    #   sets current node: [coord, adjacents]
    goal_current = graph_main[goal_num]

    #   to generate the path
    parents_front = {current_state: ""}    #parents --> path

    #   to generate the path
    parents_back = {goal_num: ""}    #parents --> path

    #   explored set up with pathcosts
    explored_start = {current_state: 0}   #holds path costs + depth

    #   dictionary to store states in path
    explored_back = {goal_num: 0}

    #   if start is already equal to goal
    if start == goal: return []

    #   if not then run A* search
    else:
        frontier_start.append((heuristic(current_state, goal_num, graph_main), current_state))   #appends the node to the frontier (h, node that holds adjacents)

        frontier_goal.append((heuristic(goal_num, current_state, graph_main), goal_num))

        while(frontier_start and frontier_goal):   #while the frontier isn't empty
            current_state_start = frontier_start.pop()
            current_state_start = current_state_start[1]
            current_start = graph_main[current_state_start]  # returns the node with the matching number as start side

            current_state_end = frontier_goal.pop()
            current_state_end = current_state_end[1]
            current_end = graph_main[current_state_end]  # returns the node with the matching number as end side

            if (current_state_end == current_state_start):
                return generate_path_bidirec(parents_front, parents_back, current_state_start, goal_num, name_dictionary,
                                             graph_main)  # returns the path

            adjacents_front = current_start[1]   #access the adjacents
            adjacents_back = current_end[1]  # access the adjacents

            for a in adjacents_front:    #goes through adjacent values
                g = explored_start[current_state_start] + 1   #calc g by value or current id

                if(a not in explored_start or g < explored_start[a]):
                    explored_start[a] = g  # adds to costs (depths) by node id

                    h = heuristic(a, goal_num, graph_main)  #calc h
                    f = explored_start[a] + h   # calculates f(n)

                    parents_front[a] = current_state_start    #adds to parents
                    frontier_start.append((f, a)) #adds to frontier,... a new node

                if (a in frontier_start and a in frontier_goal and a in explored_back):
                    return generate_path_bidirec(parents_front, parents_back, a, goal_num, name_dictionary, graph_main)  # returns the path

            for b in adjacents_back:    #goes through adjacent values
                g = explored_back[current_state_end] + 1   #calc g by value or current id

                if(b not in explored_back or g < explored_back[b]):
                    explored_back[b] = g  # adds to costs (depths) by node id
                    h = heuristic(b, current_state, graph_main)  #calc h
                    f = explored_back[b] + h   # calculates f(n)
                    parents_back[b] = current_state_end    #adds to parents
                    frontier_goal.append((f, b))  #adds to frontier,... a new node

                if(b in frontier_start and b in frontier_goal and b in explored_start):
                    return generate_path_bidirec(parents_front, parents_back, b, goal_num, name_dictionary, graph_main)  # returns the path

    return []


def tridirectional_search(start, goals, graph):
    # TODO: Do this! Good luck!

    #   creates list for the goals after user input
    list_of_goals = goals.split(",")

    #   name dictionary
    name_dictionary = graph[0]

    #   graph actual
    graph_main = graph[1]

    #   goal id numbers
    goal_id_a = name_dictionary[list_of_goals[0]]   #first node = starting
    goal_id_b = name_dictionary[list_of_goals[1]]   #middle node = mid
    goal_id_c = name_dictionary[list_of_goals[2]]   #second node = goal

    path_ab = bidirectional_a_star(goal_id_a, goal_id_b, graph) #first half
    path_bc = bidirectional_a_star(goal_id_b, goal_id_c, graph)  #second half


    path = path_ab[0] + path_bc[0]    #adds the two trial paths, not repeating the node
    path.remove(goal_id_b)  #removes duplicate
    num_exp = path_ab[1] + path_bc[1] - 1 #adds the number explored twice
    city_path_list = path_ab[3] + path_bc[3]  #city path list
    city_path_list.remove(list_of_goals[1]) #removes duplicate
    cost_sum = path_ab[2] + path_bc[2]    #adds up the cost

    return [path, num_exp, cost_sum, city_path_list]    #returns values


def main():
    start = input("Start city: ")
    goal = input("Goal city: ")

    '''depends on your data setup, you can change this part'''
    graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")

    print("\nBFS Summary")
    cur_time = time.time()
    bfs_path = breadth_first_search(start, goal, graph)
    next_time = time.time()
    print("Cost: ", bfs_path[2])
    print("Node Path: ", bfs_path[0])
    print("Number of explored: ", bfs_path[1])
    print("BFS Path: ", bfs_path[3])  #city path
    print("BFS Duration: ", (next_time - cur_time))

    print("\nA* Search Summary")
    cur_time = time.time()
    a_star_path = a_star(start, goal, graph)
    next_time = time.time()
    print("Cost: ", a_star_path[2])
    print("Node Path: ", a_star_path[0])
    print("Number of explored: ", a_star_path[1])
    print("A* Path: ", a_star_path[3])  #city path
    print("A* Duration: ", (next_time - cur_time))

    print("\nBi-directional BFS Summary")
    cur_time = time.time()
    bi_path = bidirectional_BFS(start, goal, graph)
    next_time = time.time()
    print("Cost: ", bi_path[2])
    print("Node Path: ", bi_path[0])
    print("Number of explored: ", bi_path[1])
    print("Bi-directional BFS Path: ", bi_path[3])  #city path
    print("Bi-directional BFS Duration: ", (next_time - cur_time))

    print("\nBi-directional A* Summary")
    cur_time = time.time()
    bi_a_path = bidirectional_a_star(start, goal, graph)
    next_time = time.time()
    print("Cost: ", bi_a_path[2])
    print("Node Path: ", bi_a_path[0])
    print("Number of explored: ", bi_a_path[1])
    print("Bi-directional A* Path: ", bi_a_path[3])  #city path
    print("Bi-directional A* Duration: ", (next_time - cur_time))

    # TODO: check your tridirectional search algorithm here
    print("\nTri-directional A* Summary")
    goalz = input("Input three cities, separated by comma: ")
    cur_time = time.time()
    tri_a_path = tridirectional_search(start, goalz, graph)
    next_time = time.time()
    print("Cost: ", tri_a_path[2])
    print("Node Path: ", tri_a_path[0])
    print("Number of explored: ", tri_a_path[1])
    print("Tri-directional A* Path: ", tri_a_path[3])  #city path
    print("Tri-directional A* Duration: ", (next_time - cur_time))

if __name__ == '__main__':
    main()