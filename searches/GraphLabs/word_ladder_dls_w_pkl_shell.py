import pickle

''' Node class or helper methods '''

# you can modify this method or not using it
def generate_path(current, explored):
   list = [current]
   count = 0
   while explored[current] != "":       #assume the parent of root is ""
      list.append(explored[current])
      current = explored[current]
      count += 1
   return (list[::-1], count+1)

# you can change the arguments
def recur(start, end, word_dict, explored, limit):
   ''' your code goes here '''
   return None
 
 
def solve(start, end, word_dict, limit):
   ''' you can modify this method '''
   explored = {start:""}
   return recur(start, end, word_dict, explored, limit)

def main():
   initial = input("Type the starting word: ")
   goal = input("Type the goal word: ")
   word_dict = {}
   with open("words_dict.pkl", "rb") as infile:
      word_dict = pickle.load(infile)
   limit = 9
   path_and_steps = (solve(initial, goal, word_dict, limit))
   if path_and_steps != None:
      print ("Path:", path_and_steps[0])
      print ("steps:", path_and_steps[1])

if __name__ == '__main__':
   main()
