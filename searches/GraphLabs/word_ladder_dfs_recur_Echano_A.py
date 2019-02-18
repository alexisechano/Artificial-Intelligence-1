#   Alexis Echano Period 7
#   NOT USING PICKLE, BUT GENERATING A DICTIONARY EVERYTIME

import random
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

def generate_path(start, goal, explo):    #   generates list of path words, last step
    l = []
    onState = goal
    while (onState != "start"): # parent of the state after initial state is initial state
        l.append(onState)
        onState = explo[onState]
    return l[::-1]

def recursiveDFS(start, end, d):
    explo = {}
    explo[start] = "start"
    return generate_path(start, end, DFSRecurHelper(start, explo, end, d))

def DFSRecurHelper(state, explored, goal, d):
    if(state == goal):
        return explored
    else:
        for child in d[state]:
            if(child not in explored):
                explored[child] = state
                result = DFSRecurHelper(child, explored, goal, d)
                if(result != "FAIL"):
                    return result
    return "FAIL"


#   main method for running
def main():
    testWord = input("Starting 6-letter word: ")    #   input words
    goalState = input("Goal word: ")    #   end word
    dict = createDict(word_list)  # creates dictionary

    if (len(testWord) == 6 and len(goalState) == 6):    #   makes sure no invalids

        shortestPath = recursiveDFS(testWord, goalState, dict)  #   actually finds path using DFS

        if(shortestPath != "No Solution"):
            print("The shortest path: ", shortestPath)  #   print shortest path
            print("The number of steps:", len(shortestPath))    #   prints length
        else:
            print("No Solution")
    else:
        print("Not valid input(s)")


if __name__ == '__main__':
    main()