#Alexis Echano
#11/14/2018
#Sudoku
from time import time
def backtrack_search(a, vars, csp, csp2, csp3):
    return backtrack_search_helper(vars, a ,csp, csp2, csp3)

def backtrack_search_helper(vars, assignment, csp, csp2, csp3):
    if(check_if_done(assignment, csp, len(vars), csp2, csp3)):
        return assignment
    if(len(assignment) == 81):
        return assignment
    var = select_var(assignment, vars)
    for i in vars[var]: #the colors

        if(check_is_valid(assignment, csp, csp2, csp3)):
            assignment[var] = i
            result = backtrack_search_helper(vars, assignment, csp, csp2, csp3)
            if(result != None):
                return result
            assignment.pop(var)
    return None

def check_if_done(current, csp, lenVar, csp2, csp3):
    if(len(current) != lenVar):
        return False
    for key in current:
        if (not check_thru_box(csp2, key, current)):
            return False
        if (not check_thru_box(csp, key, current)):
            return False
        if (not check_thru_box(csp3, key, current)):
            return False
            #if(current[stuff] == current[key]):
                #return False
    return True

def find_thing(c, thing):   #finds number in whatever constrsint c (r or c or b)
    for t in c:
        if(thing in t):
            return t
    return []

def check_thru_box(csp, thing, a):
    box = find_thing(csp, thing)
    s = []
    for b in box:
        if(b in a and a[b] not in s):
            s.append(a[b])
        elif(b in a and a[b] in s):
            return False
    return True


def check_is_valid(a, csp, csp2, csp3):  #check if color is not equal to any of the neighbors
    for adj in a.keys():
        if(not check_thru_box(csp2, adj, a)):
            return False
        if(not check_thru_box(csp, adj, a)):
            return False
        if (not check_thru_box(csp3, adj, a)):
            return False

    return True

def select_var(a, v):   #a = assignment
    if(len(a) == 0):
        return 0
    for val in v.keys():
        if(val not in a):
            return val
    return 80

def create_vars():
    rs = {}
    for i in range(0,81):
        rs[i] = [1,2,3,4,5,6,7,8,9]
    return rs

def print_thing(a):
    for i in range(0, 3):
        print(i, end=' ')
    print("", end=' ')
    for i in range(3, 6):
        print(i, end=' ')
    print("", end=' ')
    for i in range(6, 9):
        print(i, end=' ')
    print("", end=' ')

    print("")

    for i in range(9, 12):
        print(i, end=' ')
    print("", end=' ')
    for i in range(12, 15):
        print(i, end=' ')
    print("", end=' ')
    for i in range(15, 18):
        print(i, end=' ')
    print("", end=' ')

    print("")

    for i in range(18, 21):
        print(i, end=' ')
    print("", end=' ')
    for i in range(21, 24):
        print(i, end=' ')
    print("", end=' ')
    for i in range(24, 27):
        print(i, end=' ')
    print("", end=' ')

    print("")

    print(" ")

    for i in range(27, 30):
        print(i, end=' ')
    print("", end=' ')
    for i in range(30, 33):
        print(i, end=' ')
    print("", end=' ')
    for i in range(33, 36):
        print(i, end=' ')
    print("", end=' ')

    print("")

    for i in range(36, 39):
        print(i, end=' ')
    print("", end=' ')
    for i in range(39, 42):
        print(i, end=' ')
    print("", end=' ')
    for i in range(42, 45):
        print(i, end=' ')
    print("", end=' ')

    print("")

    for i in range(45, 48):
        print(i, end=' ')
    print("", end=' ')
    for i in range(48, 51):
        print(i, end=' ')
    print("", end=' ')
    for i in range(51, 54):
        print(i, end=' ')
    print("", end=' ')

    print("")
    print(" ")

    for i in range(54, 57):
        print(i, end=' ')
    print("", end=' ')
    for i in range(57, 60):
        print(i, end=' ')
    print("", end=' ')
    for i in range(60, 63):
        print(i, end=' ')
    print("", end=' ')

    print("")

    for i in range(63, 66):
        print(i, end=' ')
    print("", end=' ')
    for i in range(66, 69):
        print(i, end=' ')
    print("", end=' ')
    for i in range(69, 72):
        print(i, end=' ')
    print("", end=' ')

    print("")

    for i in range(72, 75):
        print(i, end=' ')
    print("", end=' ')
    for i in range(75, 78):
        print(i, end=' ')
    print("", end=' ')
    for i in range(78, 81):
        print(i, end=' ')
    print("", end=' ')

    print("")


def create_boxes(string):   #indexes
    current = {}

    stuffs = [[[0,9,18,27,36,45,54,63,72],[],[],[],[],[],[],[],[]],
              [[], [], [], [], [], [], [], [], []],
              [[0,1,2,9,10,11,18,19,20], [3,4,5,12,13,14,21,22,23], [6,7,8,15,16,17,24,25,26],
               [27,28,29,36,37,38,45,46,47], [30,31,32,39,40,41,48,49,50], [33,34,35,42,43,44,51,52,53],
               [54,55,56,63,64,65,72,73,74], [57,58,59,66,67,68,75,76,77], [60,61,62,69,70,71,78,79,80]]]   #rows, cols, boxes

    count = 1
    while count < 9:    #rows
        for x in stuffs[0][count-1]:
            stuffs[0][count].append(x+1)
        count+=1

    count = 0
    for y in range(0, 81):  #cols
        stuffs[1][count].append(y)
        if(y%9 == 8):
            count+=1

    for i in range(0, len(string)):
        if(string[i] != '.'):
            current[i] = int(string[i])
    return stuffs, current

string = input("Enter Puzzle: ")


map = create_boxes(string)

vars = create_vars()

rows = map[0][0]
cols = map[0][1]
boxes = map[0][2]

assignment = map[1]

start = time()
solution = backtrack_search(assignment,vars, rows, cols, boxes)
print_thing(solution)
print("Time:" + str(time()-start))





