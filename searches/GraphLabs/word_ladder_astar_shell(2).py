# Name:          Date:
import math, random, time, heapq

class PriorityQueue():
   """Implementation of a priority queue 
   to store nodes during search."""
   # TODO 1 : finish this class
   
   # HINT look up/use the module heapq.

   def __init__(self):
      self.queue = []
      self.current = 0    

   def next(self):
      if self.current >=len(self.queue):
         self.current
         raise StopIteration
   
      out = self.queue[self.current]
      self.current += 1
   
      return out

   def pop(self):
      # Your code goes here
      return (0, '')
   
       
   def remove(self, nodeId):
     # Your code goes here
      return (0, '')

   def __iter__(self):
      return self

   def __str__(self):
      return 'PQ:[%s]'%(', '.join([str(i) for i in self.queue]))

   def append(self, node):
      # Your code goes here
      print ('Not implemented yet')      
       
   def __contains__(self, key):
      self.current = 0
      return key in [n for v,n in self.queue]

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
      a = random.randint(0,10000)
      pq.append((a,'a'))
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
   adj_set = set()
   # TODO 2: adjacents
   # Your code goes here
   return adj_set

def dist_heuristic(v, goal):
   ''' v is the current node. Calculate the heuristic function
   and then return a numeric value'''
   # TODO 3: heuristic
   # Your code goes here
   return 0

def a_star(word_list, start, goal, heuristic=dist_heuristic):
   '''A* algorithm use the sum of cumulative path cost and the heuristic value for each loop
   Update the cost and path if you find the lower-cost path in your process.
   You may start from your BFS algorithm and expand to keep up the total cost while moving node to node.
   '''
   frontier = PriorityQueue()
   if start == goal: return []
   # TODO 4: A* Search
   # Your code goes here
   return None

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
      print (path_and_steps)
      print ("steps: ", len(path_and_steps))
      print ("Duration: ", time.time() - cur_time)
   else:
      print ("There's no path")
 
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
steps:  21
Duration:  0.0867915153503418
'''


