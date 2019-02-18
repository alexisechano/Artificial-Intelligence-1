#   Alexis Echano Period 7
#   Word Ladder Lab 3
#   USING PICKLE

import random
import pickle
from collections import deque

word_list = open('words.txt','r').read().split()

def createDict(wlist):  #   creates dictionary of adjacent words using word_list and findLikeWords
    dWords = {}

    for word in word_list:
        dWords[word] = findLikeWords(word, word_list)

    return dWords

def findLikeWords(w, listw):    #    creates list of words that have a single letter difference from w
    likeWords = []

    for x in listw:
        if(costCalc(w, x) == 1):
            likeWords.append(x)
    return likeWords

def costCalc(w1, w2):   #   cost calc determines if only one letter differs cost == 1
    cost = 0
    for i in range(len(w1)):
        if(w1[i] != w2[i]):
            cost+=1
    return cost

def generate_path(current, explored):
   list = [current]
   count = 0
   while explored[current] != "":       #assume the parent of root is ""
      list.append(explored[current])
      current = explored[current]
      count += 1
   return (list[::-1], count+1)

def BFsearch(start, end, d):
    #   dictionary to store states in path
    explored = {start:""}

    #   creates queue for frontier
    frontier = deque()

    # adds initial state to the Deque
    frontier.append(start)

    #   sets the current state at the initial
    current_state = start

    #   loop runs until the queue is empty or NO SOLUTION
    while (len(frontier) != 0):
        #   explored then adds the current state
        #   pops the FIFO (so the first in the queue)
        current_state = frontier.popleft()

        if (current_state == end):  #   checks goal state and prints out the path
            return generate_path(current_state, explored)
        else:
            childs = d[current_state]  # returns list of children/adjacent words and sets to childs

            #   for every newly generated child, it checks each new state if added to explored
            for child in childs:
                if (child not in explored.keys()):
                    frontier.append(child)
                    explored[child] = current_state     #   child: parent added to dictionary

    #   returns no solution
    return("No Solution")

#   main method for running
def main():
    testWord = input("Starting 6-letter word: ")    #   input words
    goalState = input("Goal word: ")    #   end word

    if (len(testWord) == 6 and len(goalState) == 6):    #   makes sure no invalids
        # Load data
        with open('words_dict.pickle', 'rb') as handle:
            dataDict = pickle.load(handle)

        shortestPath = BFsearch(testWord, goalState, dataDict)  #   actually finds path using BFS

        if(shortestPath != "No Solution"):
            print("The shortest path: ", shortestPath[0])  #   print shortest path
            print("The number of steps:", shortestPath[1]  )    #   prints length
        else:
            print("No Solution")
    else:
        print("Not valid input(s)")

if __name__ == '__main__':
    main()
