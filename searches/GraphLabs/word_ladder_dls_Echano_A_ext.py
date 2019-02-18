#   Alexis Echano P7
#   DLS Word Ladder Extension (ITERATIVE, NOT OPTIMIZED FOR >18)

import random
from collections import deque
import pickle


def generate_path(current, explored):  # generates path using explored and current state
    list = [current]
    count = 0
    while explored[current] != "":  # assume the parent of root is ""
        list.append(explored[current])
        current = explored[current]
        count += 1
    return (list[::-1], count + 1)



def cur_path(cur, explored):  # finds set of current nodes in explored
    p = set(cur)
    while (explored[cur] != ""):
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

def iterDLS(start, goal, d):  # recurs DLS but with iterative deepening
    explo = {start: ""}
    limit = 0
    test = DLS_recur_helper(start, explo, goal, d, limit)
    while(test == None or limit >= 18):    #until something is found, it increments limit (until 18)
        limit += 1
        test = DLS_recur_helper(start, explo, goal, d, limit)
    return test


#   main method for running
def main():
    testWord = input("Starting 6-letter word: ")  # input words
    goalState = input("Goal word: ")  # end word

    if (len(testWord) == 6 and len(goalState) == 6):  # makes sure no invalids
        # Load data using pickle
        with open('words_dict.pickle', 'rb') as handle:
            dataDict = pickle.load(handle)

        shortestPath = iterDLS(testWord, goalState, dataDict)  # actually finds path using DFS

        if (shortestPath != None):
            print("The shortest path: ", shortestPath[0])  # print shortest path
            print("The number of steps:", shortestPath[1])  # prints length
        else:
            print("No Solution")
    else:
        print("Not valid input(s)")


if __name__ == '__main__':
    main()