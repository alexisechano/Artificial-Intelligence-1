#   Alexis Echano

from collections import deque
def swap(state, i, j):  #swaps two characters in a string
    str = state[:i] + state[j] + state[i+1:j] + state[i] + state[j+1:]
    return str


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

# main
def main():
    #opens file for writing:
    text_file = open("num_states_at_depth.txt", 'w')

    q = deque()
    goal_state = "_12345678"
    q.append(goal_state)
    explored = {}
    explored[q[0]] = 0

    while(len(q) != 0):
        current = q.popleft()
        childs = generate_children(current)
        for c in childs:
            if c not in explored:
                explored[c] = explored[current] + 1

    temp = []
    depths = {}
    for item in explored.keys():
        depth = explored[item]
        while(explored[item] == depth):
            temp.append(item)
        depths[depth-1] = temp


    for i in depths.keys():  #writes to text file
        d = i
        leng = len(depths[i])
        text_file.write("@ Depth: " + i + " " + leng + "\n")

    text_file.close()

if __name__ == '__main__':
    main()
