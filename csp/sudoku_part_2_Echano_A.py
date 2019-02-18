#Alexis Echano
#Sudoku Part 2
#puzzles.txt

from time import time

def backtrack_search(a, csp, empties, constraints, poss, m, n): #csp is the adjacents
    if(len(empties) == 0):
        return a
    return backtrack_search_helper(empties, a, csp, empties[0], m, n)

def backtrack_search_helper(empties, assignment, csp,  c, m, n):  #figure out restoration and updating
    if(len(assignment)== (m*m*n*n)):
        return assignment
    else:
        var = select_var(empties, assignment, c, csp,  m, n)    #chooses value, UPDATE HERE

        possibles = var[1]  #list of ALREADY VALIDITY CHECKED VALUES
        curr = var[0]   #current value

        for i in possibles:
            assignment[curr] = i
            result = backtrack_search_helper(empties, assignment, csp, curr,  m, n)
            if(result != None):
                return result
            assignment.pop(curr)

        return None

def determine_best(value, csp, constraints, possiblez):
    return possiblez

def checkSum(pzl, len):
    sum = 0
    for i in pzl.keys():
        sum += ord(str(pzl[i]))
    return sum - (48*len)

def determine_possibles(value, assignment, csp, constraints, x):  #for non solved, csp are adjacents
    current_neighbors = csp[value]  #retreives adjacent set

    possible_numbers = set()
    if(x == 9):
        possible_numbers.update(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    if(x == 12):
        possible_numbers.update(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C'])
    if(x == 16):
        possible_numbers.update(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G'])

    items = {assignment[number] for number in current_neighbors if number in assignment}

    temp_domain = possible_numbers - items
    return temp_domain

def select_var(e, a, curr, csp, m, n):   #a = assignment #put possibilities and already checks valid

    real_list = []
    real_val = curr

    shortest_len = 18

    i = 0

    while i < len(e):
        if(e[i] not in a.keys()):

            val = e[i]
            new_list = determine_possibles(val, a, csp, {}, m*n)

            if(len(new_list) == 1):
                return val, new_list

            if(len(new_list) < shortest_len and len(new_list) >= 0):
                shortest_len = len(new_list)
                real_val = val
                real_list = new_list
        i += 1
    return real_val, real_list


#administrative stuff
def print_thing(a, c): #prints in to proper format
    result = "["

    for value in a.keys():
        result = result + str(a[value])

    result = result + ", " + str(c) + "]"
    print(result)

def adjacents(val,rows, cols, boxes):    #look up table/CSP, val is index
    adjacent_set = set()

    for row in rows:
        if(val in row):
            adjacent_set.update(row)
            break

    for col in cols:
        if(val in col):
            adjacent_set.update(col)
            break

    for box in boxes:
        if(val in box):
            adjacent_set.update(box)
            break

    if(val in adjacent_set):
        adjacent_set.remove(val)

    return adjacent_set

def set_up(line_length, m, n):
    #   technically the CSP stuff
    rows = []
    cols = []
    boxes = []

    for i in range(m*n):
        rows.append(set())
        cols.append(set())
        boxes.append(set())

    row_tracker = 0

    j = 0
    while j < line_length:
        col_number = j % (m*n)

        cols[col_number].add(j)  # adds to proper column set
        rows[row_tracker].add(j)  # adds to proper row set in list

        if (j % (m*n) == ((m*n) -1)):  # keeps track of rows
            row_tracker += 1

        box_num = int(m * (j // (m*m*m)) + (j % (m*n)) // n)  # keeps track of sub-boxes
        boxes[box_num].add(j)

        j += 1

    return rows, cols, boxes

def create_boxes(line, r, c, b, m, n):   #create sets and use adjaents to create look up table
    curr_list = []   #map usage since indexes can be values
    start_state = {}  #dictionary to print first state
    possibs = {}
    look_up_table = {}  #key is the index and set is the value of adjacents

    for i in range(0, len(line)): #only fill in the knowns
        if(line[i] == '.'):
            curr_list.append(i)
        else:
            start_state[i] = line[i] #adds to empty list for solving

    for y in range(0,len(line)):    #builds variables
        if(y in curr_list):
            look_up_table[y] = adjacents(y, r, c, b)
            possibs[y] = determine_possibles(y, start_state, look_up_table, {}, m* n)

    return look_up_table, curr_list, start_state, possibs

def determine_dimensions(length):
    if(length == 144):
        return 4,3  #4x3 "****
                    #     ****
                    #     ****"
    elif(length == 256):
        return 4,4
    return 3,3

def main_method():
    file = input("Enter filename: ").lower()
    file_contents = open(file, 'r').read().split()
    puz_num = 1
    total_time = time()

    checka = len(file_contents[0])
    m, n = determine_dimensions(checka)

    rows, cols, boxes = set_up(checka, m, n)

    while(len(file_contents) > 0):
        print("- - - - - - - - - -")
        print("Puzzle #" + str(puz_num), end=' ')

        current_puzzles = list(file_contents.pop(0))    #sets up boxes and stuff

        map = create_boxes(current_puzzles, rows, cols, boxes, m , n)  #list of lists

        adjs = map[0]   #csp
        empties = map[1]    #what the program will actually use
        assignment = map[2] #the already solved parts of the board
        constraints = {}   #collects data on how many open spaces for each symbol, updates each time
        poss = map[3]   #replica of empties but with lists of variables

        t = time()  # begins time
        solution = backtrack_search(assignment, adjs, empties, constraints, poss, m, n)

        print_thing(solution, checkSum(solution, checka))
        print('Time: ' + str(time() - t))   #ends time
        print("Total Time: " + str(time() - total_time)) #total time elapsed

        puz_num += 1    #goes to next puzzle


#runs this baby
main_method()