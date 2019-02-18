#   Alexis Echano P7
#   DLS 8 Puzzle

import random
from collections import deque

def swap(state, i, j):  #swaps two characters in a string
    str = state[:i] + state[j] + state[i+1:j] + state[i] + state[j+1:]
    return str


'''Generate a list which hold all children of the current state
   and return the list'''


def generate_children(state):
    #   creates new list to return later
    children = []

    #   finds index of the blank
    index_of_blank = state.index('_')

    #   booleans to check if the bounds will allow movement
    canMoveU = True
    canMoveD = True
    canMoveL = True
    canMoveR = True

    if (index_of_blank <= 2):  # top side -- blank cannot move up
        canMoveU = False
    if (index_of_blank % 3 == 0):  # left side -- blank cannot move left
        canMoveL = False
    if ((index_of_blank + 1) % 3 == 0):  # right side -- blank cannot move right
        canMoveR = False
    if ((index_of_blank) >= 6):  # bottom side -- blank cannot move down
        canMoveD = False

    #   using the booleans above, the newly generated children append to the list
    if (canMoveU):
        children.append(swap(state, index_of_blank - 3, index_of_blank))
    if (canMoveD):
        children.append(swap(state, index_of_blank, index_of_blank + 3))
    if (canMoveL):
        children.append(swap(state, index_of_blank - 1, index_of_blank))
    if (canMoveR):
        children.append(swap(state, index_of_blank, index_of_blank + 1))

    #   returns list of children
    return children

def generate_path(current, explored):   # generates path using explored and current state
   list = [current]
   count = 0
   while explored[current] != "":       #assume the parent of root is ""
      list.append(explored[current])
      current = explored[current]
      count += 1
   return (list[::-1], count+1)

def recursive_DLS(start, end):   #solves
    explo = {start: ""}
    limit = int(input("Enter limit: "))
    return DLS_recur_helper(start, explo, end, limit)

def cur_path(cur, explored):    #finds set of current nodes in explored
    p = set(cur)
    while(explored[cur] != ""):
        p.add(explored[cur])
        cur = explored[cur]

    return p

def DLS_recur_helper(start, explored, goal, limit):  #recurs DLS
    if(start == goal):
        return generate_path(goal, explored)
    elif(limit == 0):
        return None
    else:
        for adj in generate_children(start):
            if adj not in cur_path(start, explored):
                explored[adj] = start
                result = DLS_recur_helper(adj, explored, goal, limit-1)
                if(result != None):
                    return result
    return None

#   main method for running
def main():
    initialState = input("Starting state: ")    #   input words
    goalState = "_12345678"

    if (len(initialState) == 9):    #   makes sure no invalids

        shortestPath = recursive_DLS(initialState, goalState)  #   actually finds path using DFS

        if(shortestPath != None):
            print("The shortest path: ", shortestPath[0])  #   print shortest path
            print("The number of steps:", shortestPath[1])    #   prints length
        else:
            print("No Solution")
    else:
        print("Not valid input(s)")


if __name__ == '__main__':
    main()