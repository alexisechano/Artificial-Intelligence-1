# Name: Alexis Echano          Date: 10/5/2018
import math, random, time, heapq


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
        return(node)     #returns popped value which is a tuple

    def remove(self, nodeId):   #removes at certain index
        item = self.queue.pop(self, nodeId)
        return (item)  #returns popped value which is a tuple

    def __iter__(self):
        return self

    def __str__(self):
        return 'PQ:[%s]' % (', '.join([str(i) for i in self.queue]))

    def append(self, node):
        heapq.heappush(self.queue, node)    #using heappq method, node is added according to cost in to PQ

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

def generate_adjacents(current, word_list):
    ''' word_list is a set which has all words.
    By comparing current and words in the word_list,
    generate adjacents set and return it'''
    adj_list = set()    #creates a new set
    # TODO 2: adjacents
    alpha = "abcdefghijklmnopqrstuvwxyz"    #variable to store alphabet
    for i in range(len(current)):   #loops through the word current
        for j in alpha: #for every letter in the alphabet
            word = current[:i] + j + current[i+1:]  #creates a new word with that letter
            if word != current and word in word_list:   #checks if the created word is an adjacent
                adj_list.add(word)  #adds the new word
    return adj_list #returns the set of adjacents

def cost_calc(w1, w2):   # cost calc determines if only one letter differs cost == 1
    cost = 0    #initializes cost variable
    for i in range(len(w1)):    # for every char in the given word
        if(w1[i] != w2[i]): # checks if the character equals the same index of the other
            cost+=1 #adds to cost var
    return cost #returns cost

def dist_heuristic(v, goal):    #heuristic will be letters different that goal word
    ''' v is the current node. Calculate the heuristic function
    and then return a numeric value'''
    # TODO 3: heuristic
    return cost_calc(v, goal)   #again uses cost calc to determine letters different from goal


def a_star(word_list, start, goal, heuristic=dist_heuristic):
    '''A* algorithm use the sum of cumulative path cost and the heuristic value for each loop
    Update the cost and path if you find the lower-cost path in your process.
    You may start from your BFS algorithm and expand to keep up the total cost while moving node to node.
    '''
    frontier = PriorityQueue()  #initiates a frontier

    explored = set()    #creates a new set for explored: mainly for efficiency purposes
    explored.add(start) #adds the first word to explored

    if start == goal: return [] #if the start equals the goal, returns a blank path
    # TODO 4: A* Search
    # Your code goes here

    else:
        cost = heuristic(start, goal)   #calculates the g (which is 0) + h (generates heuristic)
        curr = (cost, start, [start])    #Created tuple node: (cost, value, [path])
        frontier.append(curr)   #appends the node to the frontier

        while(frontier.size() > 0):   #while the frontier isn't empty
            curr = frontier.pop()  #pops the priority value
            val = curr[1]   #accesses the node value using the tuple
            path = curr[2]  #accesses the current path using the tuple

            #explored.add(val)
            # check if a path is found
            if(val == goal):
                return path #returns the path

            for c in generate_adjacents(val, word_list):    #goes through adjacent values
                tempPath = list(path) #creates new path based on previous
                tempPath.append(c)  #adds the child to the path

                if(c not in explored):  #if the child is not in the set explored
                    new_cost = (curr[0] + 1) + cost_calc(val, c) + heuristic(c, goal) #calculates cost based on previous cost,
                                                                                #current cost and then the heuristic function
                    new_node = (new_cost, c, tempPath)  #creates new tuple node
                    frontier.append(new_node)   #adds to froniter
                    explored.add(c) #adds word to explored

    return None #if nothing is found, return none

def main():
    word_list = set()
    file = open("words_6_longer.txt", "r")
    for word in file.readlines():
        word_list.add(word.rstrip('\n'))
    file.close()
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    cur_time = time.time()
    path_and_steps = (a_star(word_list, initial, goal))
    if path_and_steps != None:
        print(path_and_steps)
        print("steps: ", len(path_and_steps))
        print("Duration: ", time.time() - cur_time)
    else:
        print("There's no path")


if __name__ == '__main__':
    main()


'''Sample output 1
Type the starting word: listen
Type the goal word: beaker
['listen', 'lister', 'bister', 'bitter', 'better', 'beater', 'beaker']
steps:  7
Duration: 0.000997304916381836

Sample output 2
Type the starting word: vaguer
Type the goal word: drifts
['vaguer', 'vagues', 'values', 'valves', 'calves', 'cauves', 'cruves', 'cruses', 'crusts', 'crufts', 'crafts', 'drafts', 'drifts']
steps:  13
Duration: 0.0408782958984375

Sample output 3
Type the starting word: klatch
Type the goal word: giggle
['klatch', 'clatch', 'clutch', 'clunch', 'glunch', 'gaunch', 'launch', 'launce', 'paunce', 'pawnce', 'pawnee', 'pawned', 'panned', 'panged', 'banged', 'bunged', 'bungee', 'bungle', 'bingle', 'gingle', 'giggle']
steps:  19
Duration:  0.0867915153503418
'''


