import random
from collections import deque

def getInitialState():
    x = "_12345678"
    l = list(x)
    random.shuffle(l)
    y = ''.join(l)
    return y

'''precondition: i<j
   swap characters at position i and j and return the new state'''


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


def generate_path(n, explored):
    l = []
    onState = n
    while (onState != "initial state"): # parent of the state after initial state is initial state
        l.append(onState)
        onState = explored[onState]
    print()
    l = l[::-1]
    for i in l:
        print(i[0:3], end="   ")
    print()
    for j in l:
        print(j[3:6], end="   ")
    print()
    for k in l:
        print(k[6:9], end="   ")
    print("\n\nThe shortest path length is :", len(l) - 1)  #   -1 is to get rid of first state
    return ""


'''Find the shortest path to the goal state "_12345678" and
   returns the path by calling generate_path() function to print all steps.
   You can make other helper methods, but you must use dictionary for explored.'''

def BFS(initial):
    #   dictionary to store states in path
    explored = {}
    #   creates queue for frontier
    frontier = deque()

    frontier.append(initial)  # adds initial state to the Deque

    #   sets the current state at the initial
    current_state = initial
    #   loop runs until the queue is empty or NO SOLUTION
    while (len(frontier) != 0):
        #   explored then adds the current state
        if(current_state not in explored.keys()):
            explored[current_state] = "initial state"

        if (current_state == "_12345678"):  #   checks goal state and prints out the output
            return generate_path(current_state, explored)
        else:
            childs = generate_children(current_state)  # returns list of children and sets to childs

            #   for every newly generated child, it checks each new state if added to explored
            for child in childs:
                if (child not in explored.keys()):
                    frontier.append(child)
                    explored[child] = current_state     #   child: parent added to dictionary

            #   pops the FIFO (so the first in the queue)
            current_state = frontier.popleft()

    #   returns no solution
    print("No Solution")


'''Find the shortest path to the goal state "_12345678" and
   returns the path by calling generate_path() function to print all steps.
   You can make other helper methods, but you must use dictionary for explored.'''


def DFS(initial):
    #   dictionary to store states in path
    explored = {}
    #   creates stack for frontier
    frontier = []

    frontier.append(initial)  # adds initial state to the Deque

    #   sets the current state at the initial
    current_state = initial
    #   loop runs until the queue is empty or NO SOLUTION
    while (len(frontier) != 0):
        #   explored then adds the current state
        if(current_state not in explored.keys()):
            explored[current_state] = "initial state"

        if (current_state == "_12345678"):  #   checks goal state and prints out the output
            return generate_path(current_state, explored)
        else:
            childs = generate_children(current_state)  # returns list of children and sets to childs

            #   for every newly generated child, it checks each new state if added to explored
            for child in childs:
                if (child not in explored.keys()):
                    frontier.append(child)
                    explored[child] = current_state     #   child: parent added to dictionary

            #   pops the stack
            current_state = frontier.pop()

    #   returns no solution
    print("No Solution")


def main():
    initial = getInitialState()
    print("BFS start with:\n", initial[0:3], "\n", initial[3:6], "\n", initial[6:], "\n")
    print(BFS(initial))
    print("DFS start with:\n", initial[0:3], "\n", initial[3:6], "\n", initial[6:], "\n")
    print(DFS(initial))


if __name__ == '__main__':
    main()