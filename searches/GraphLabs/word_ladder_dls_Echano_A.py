#   Alexis Echano P7
#   DLS Word Ladder

import random
from collections import deque
import pickle


def generate_path(current, explored):   # generates path using explored and current state
   list = [current]
   count = 0
   while explored[current] != "":       #assume the parent of root is ""
      list.append(explored[current])
      current = explored[current]
      count += 1
   return (list[::-1], count+1)

def recursive_DLS(start, end, d):   #solves
    explo = {start: ""}
    limit = int(input("Enter limit: "))
    return DLS_recur_helper(start, explo, end, d, limit)

def cur_path(cur, explored):    #finds set of current nodes in explored
    p = set(cur)
    while(explored[cur] != ""):
        p.add(explored[cur])
        cur = explored[cur]

    return p

def DLS_recur_helper(start, explored, goal, d, limit):  #recurs DLS
    if(start == goal):
        return generate_path(goal, explored)
    elif(limit == 0):
        return None
    else:
        for adj in d[start]:
            if adj not in cur_path(start, explored):
                explored[adj] = start
                result = DLS_recur_helper(adj, explored, goal, d, limit-1)
                if(result != None):
                    return result
    return None

#   main method for running
def main():
    testWord = input("Starting 6-letter word: ")    #   input words
    goalState = input("Goal word: ")    #   end word

    if (len(testWord) == 6 and len(goalState) == 6):    #   makes sure no invalids
        # Load data using pickle
        with open('words_dict.pickle', 'rb') as handle:
            dataDict = pickle.load(handle)

        shortestPath = recursive_DLS(testWord, goalState, dataDict)  #   actually finds path using DFS

        if(shortestPath != "No Solution"):
            print("The shortest path: ", shortestPath[0])  #   print shortest path
            print("The number of steps:", shortestPath[1])    #   prints length
        else:
            print("No Solution")
    else:
        print("Not valid input(s)")


if __name__ == '__main__':
    main()