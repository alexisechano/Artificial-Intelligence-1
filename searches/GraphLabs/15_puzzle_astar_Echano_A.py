# Name: Alexis Echano          Date: 10/5/2018
import heapq
import random, time, math


class PriorityQueue():
    """Implementation of a priority queue
    to store nodes during search."""

    # TODO 1 : finish this class

    # HINT look up/use the module heapq.

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


def check_pq():
    ''' check_pq is checking if your PriorityQueue
    is completed or not'''
    pq = PriorityQueue()
    temp_list = []

    for i in range(10):
        a = random.randint(0, 10000)
        pq.append((a, 'a'))
        temp_list.append(a)

    temp_list = sorted(temp_list)

    for i in temp_list:
        j = pq.pop()
        if not i == j[0]:
            return False

    return True


# Extension #1
def findInversion(size,state):   #finds inversions of state and returns value
    inversions = 0

    for i in range(((size * size)-size)):
        for j in range(1,(size * size)):
            if(state[i] > state[j]):
                inversions+=1
    return inversions

def inversion_count(new_state, size):
    ''' Depends on the size(width, N) of the puzzle,
    we can decide if the puzzle is solvable or not by counting inversions.
    If N is odd, then puzzle instance is solvable if number of inversions is even in the input state.
    If N is even, puzzle instance is solvable if
       the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) and number of inversions is odd.
       the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) and number of inversions is even.
    '''
    inv = findInversion(new_state)  #finds inversion value of each state
    if(inv%2 == 0): #if in version is even , it is solvable
        return True


def getInitialState(sample):
    sample_list = list(sample)
    random.shuffle(sample_list)
    new_state = ''.join(sample_list)
    if (inversion_count(new_state, 4)):
        return new_state
    else:
        return None


def swap(n, i, j):
    n = n[:i] + n[j] + n[i + 1:j] + n[i] + n[j + 1:]
    return n


def generateChild(n, size):
    #   creates new list to return later
    children = []

    #   finds index of the blank
    index_of_blank = n.index('_')

    #   booleans to check if the bounds will allow movement
    canMoveU = True
    canMoveD = True
    canMoveL = True
    canMoveR = True

    if (index_of_blank <= (size-1)):  # top side -- blank cannot move up
        canMoveU = False
    if (index_of_blank % (size) == 0):  # left side -- blank cannot move left
        canMoveL = False
    if ((index_of_blank + 1) % (size) == 0):  # right side -- blank cannot move right
        canMoveR = False
    if ((index_of_blank) >= ((size * size)-size)):  # bottom side -- blank cannot move down
        canMoveD = False

    #   using the booleans above, the newly generated children append to the list
    if (canMoveR):  #move right
        children.append(swap(n, index_of_blank, index_of_blank + 1))
    if (canMoveU):  #move up
        children.append(swap(n, index_of_blank - size, index_of_blank))
    if (canMoveD):  #move down
        children.append(swap(n, index_of_blank, index_of_blank + size))
    if (canMoveL):  #move left
        children.append(swap(n, index_of_blank - 1, index_of_blank))


    #   returns list of children
    return children


def display_path(path_list, size):
    for n in range(size):
        for i in range(len(path_list)):
            print(path_list[i][n * size:(n + 1) * size], end=" " * size)
        print()
    print("\nThe shortest path length is :", len(path_list))
    return ""

def dist_heuristic(start, goal, size, dict):
    # Your code goes here

    h = 0
    x1 = 0
    y1 = 0

    for ch in start:
        x2, y2 = dict[ch]
        h += abs(x2-x1) + abs(y2-y1)
        y1 += 1
        if(y1 == size):
            y1 = 0
            x1 += 1

    return h
'''
    cost = 0    #initializes cost variable
    for i in range(len(start)):    # for every char in the given word, i is current index, ind_w2 is the other
        cost += abs(dict[start[i]][0] - (i // size))
        cost += abs(dict[start[i]][1] - (i % size))  #adds the difference in cost
    return cost  #returns cost'''

def create_dict_graph(goal, size):  #creates graph of coordinates
    dictionary = {}

    for char in goal:
        dictionary[char] = (goal.index(char)//size, goal.index(char)%size)
    return dictionary

def gen_temp_path(current, p):    #generates path from parent dictionary
    list = [current]
    while p[current] != "":  # assume the parent of root is ""
        list.append(p[current])
        current = p[current]
    return list[::-1]

def a_star(start, goal="_123456789ABCDEF", heuristic=dist_heuristic):
    frontier = PriorityQueue()

    explored = {start: 0}   #holds path costs + depth
    parents = {start:""}    #parents --> path

    size = 4
    dictionary_graph = create_dict_graph(goal, size)

    if start == goal: return []

    else:
        cost = heuristic(start, goal, size, dictionary_graph)   #calculates the g (which is 0) + h (generates heuristic)
        frontier.append((cost, start))   #appends the node to the frontier

        while(frontier.size() > 0):   #while the frontier isn't empty
            curr = frontier.pop()  #pops the priority value

            # check if a path is found
            if(curr[1]  == goal):#accesses the node value using the tuple and checks if goal
                return gen_temp_path(curr[1], parents) #returns the path

            for c in generateChild(curr[1], size):    #goes through adjacent values
                g = explored[curr[1]] + 1   #calc g

                if(c not in explored or g < explored[c]):
                    explored[c] = g  # adds to costs (depths)
                    h = heuristic(c, goal, size, dictionary_graph)  #calc h
                    f = explored[c] + h   # calculates f(n)
                    parents[c] = curr[1]    #adds to parents
                    frontier.append((f, c))  #adds to frontier,... a new node

    return None     #if nothing is found, return none

def main():
    # check PriorityQueue
    if check_pq():
        print("PriorityQueue is good to go.")
    else:
        print("PriorityQueue is not ready.")

    # A star
    ''' This part is for extension
    initial_state = getInitialState("_123456789ABCDEF")
    while initial_state == None:
       initial_state = getInitialState("_123456789ABCDEF")
    '''
    initial_state = input("Type initial state: ")
    cur_time = time.time()
    path = (a_star(initial_state))
    if path != None:
        display_path(path, 4)
    else:
        print("No Path Found.")
    print("Duration: ", (time.time() - cur_time))


if __name__ == '__main__':
    main()

''' Sample output 1
PriorityQueue is good to go.

Initial State: 152349678_ABCDEF
1523    1523    1_23    _123    
4967    4_67    4567    4567    
8_AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 4
Duration:  0.0

Sample output 2
PriorityQueue is good to go.

Initial State: 2_63514B897ACDEF
2_63    _263    5263    5263    5263    5263    5263    5263    5263    52_3    5_23    _523    1523    1523    1_23    _123    
514B    514B    _14B    1_4B    14_B    147B    147B    147_    14_7    1467    1467    1467    _467    4_67    4567    4567    
897A    897A    897A    897A    897A    89_A    89A_    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 16
Duration:  0.005984306335449219

Sample output 3
PriorityQueue is good to go.

Initial State: 8936C_24A71FDB5E
8936    8936    8936    8936    8936    8936    8936    8936    8936    8936    8936    893_    89_3    8943    8943    8_43    84_3    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
C_24    C2_4    C214    C214    C214    C214    C214    C214    C214    C2_4    C24_    C246    C246    C2_6    C_26    C926    C926    C9_6    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    AB17    AB17    AB17    AB17    AB17    AB17    AB17    AB17    AB17    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 39
Duration:  0.27825474739074707

#E19648C5723_ABDF
'''


