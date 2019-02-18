#   Alexis Echano
#   Lab 01: 8 Puzzle DFS and BFS

from collections import deque

goal_state = "012345678"    # goal-state to compare to

#   just checks if the current state equals the goal state
def checkGoalTest(current):
    return current == goal_state

#   generate children method
def generateChildren(current):
    #   creates new list to return later
    children = []

    #   finds index of the blank
    index_of_blank = current.index('0')

    #   booleans to check if the bounds will allow movement
    canMoveU = True
    canMoveD = True
    canMoveL = True
    canMoveR = True

    if(index_of_blank <= 2):    #top side -- blank cannot move up
        canMoveU = False
    if(index_of_blank % 3 == 0):   #left side -- blank cannot move left
        canMoveL = False
    if((index_of_blank + 1) % 3 == 0):   #right side -- blank cannot move right
        canMoveR = False
    if((index_of_blank) >= 6):   #bottom side -- blank cannot move down
        canMoveD = False

    #   using the booleans above, the newly generated children append to the list
    if(canMoveU):
        children.append(up(current))
    if(canMoveD):
        children.append(down(current))
    if(canMoveR):
        children.append(right(current))
    if(canMoveL):
        children.append(left(current))

    #   returns list of children
    return children


#   moves up in board using string concatenation
def up(state):
    newState = ""
    indexSplit = state.index('0')
    newIndex = indexSplit - 3
    replace = state[newIndex]
    newState = state[:newIndex] + '0' + state[newIndex+1:indexSplit]+ replace + state[indexSplit+1:]

    return newState

#   moves down in board using string concatenation
def down(state):
    newState = ""
    indexSplit = state.index('0')
    newIndex = indexSplit + 3
    replace = state[newIndex]
    newState = state[:indexSplit] + replace + state[indexSplit+1:newIndex]+ '0' + state[newIndex+1:]

    return newState

#   moves right in board using string concatenation
def right(state):
    newState = ""
    indexSplit = state.index('0')
    state = state[:indexSplit] + state[(indexSplit + 1):]
    indexSplit = indexSplit + 1

    newState = state[:indexSplit] + '0' + state[indexSplit:]

    return newState

#   moves left in board using string concatenation
def left(state):
    newState = ""
    indexSplit = state.index('0')
    state = state[:indexSplit] + state[(indexSplit + 1):]
    indexSplit = indexSplit - 1

    newState = state[:indexSplit] + '0' + state[indexSplit:]

    return newState

#   BFS algorithm
def breadthFirstSearch(initial):
    #   creates queue for frontier
    frontier = deque()

    #   creates set for explored to get rid of duplicates
    explored = set()

    frontier.append(initial)  # adds initial state to the Deque

    #   sets the current state at the initial
    current_state = initial

    #   loop runs until the queue is empty or NO SOLUTION
    while (len(frontier) != 0):
        #   explored then adds the current state
        explored.add(current_state)
        numOfChildren = len(explored)

        if (checkGoalTest(current_state)):  # checks goal state
            return current_state, numOfChildren
        else:
            childs = generateChildren(current_state)  # returns list of children and sets to childs

            #   for every newly generated child, it checks each new state if added to explored
            for child in childs:
                if (child not in explored):
                    frontier.append(child)
                    explored.add(child)

            #   pops the FIFO (so the first in the queue)
            current_state = frontier.popleft()

    #   returns no solution
    return "No Solution", numOfChildren

def depthFirstSearch(initial):
    #   creates stack/list for frontier
    frontier = []

    #   creates set for explored to get rid of duplicates
    explored = set()

    frontier.append(initial)  # adds initial state to the Deque

    #   sets the current state at the initial
    current_state = initial

    #   loop runs until the queue is empty or NO SOLUTION
    while (len(frontier) != 0):
        #   explored then adds the current state
        explored.add(current_state)
        numOfChildren = len(explored)

        if (checkGoalTest(current_state)):  #   checks goal state
            return current_state, numOfChildren
        else:
            childs = generateChildren(current_state)  # returns list of children and sets to childs

            #   for every newly generated child, it checks each new state if added to explored
            for child in childs:
                if (child not in explored):
                    frontier.append(child)
                    explored.add(child)

            #   pops the stack
            current_state = frontier.pop()

    #   returns no solution
    return "No Solution", numOfChildren

#   main method for running
def main():

    #   user input
    initial_state = input("Enter Initial State of 8-Puzzle: ")

    #   runs BFS and DFS
    bfs_item, c2 = breadthFirstSearch(initial_state)
    dfs_item, c1 = depthFirstSearch(initial_state)

    #   prints the results
    if(bfs_item == "No solution"):
        print(bfs_item)
    if(dfs_item == "No solution"):
        print(dfs_item)

    else:
        print("Goal State: ", bfs_item)
        print("BFS Number of states expanded: ", c2)
        print(" ")
        print("Goal State: ", dfs_item)
        print("DFS Number of states expanded: ", c1)

if __name__ == '__main__':
    main()

#trial: 724506831
