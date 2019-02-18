#Alexis Echano
#11/12/2018
#Day 3, Task 1

def backtrack_search(vars, csp, csp2):
    return backtrack_search_helper(vars, {} ,csp, csp2)

def backtrack_search_helper(vars, assignment, csp, csp2):
    if(check_if_done(assignment, csp, len(vars), csp2)):
        return assignment
    if(len(assignment) == 24):
        return assignment

    var = select_var(assignment, vars)
    for i in vars[var]: #the colors

        if(check_is_valid(i, var, assignment, csp, csp2)):
            assignment[var] = i
            result = backtrack_search_helper(vars, assignment, csp, csp2)
            if(result != None):
                return result
            assignment.pop(var)
    return None

def check_if_done(current, csp, lenVar, csp2):
    if(len(current) != lenVar):
        return False
    for key in current:
        for stuff in csp[key]:
            if(not check_thru_hex(csp2,stuff, current)):
                return False
            if(current[stuff] == current[key]):
                return False
    return True

def find_thing(h, thing):
    for t in h:
        if(thing in t):
            return t
    return []


def check_thru_hex(csp, thing, a):
    hexagon = find_thing(csp, thing)
    s = []
    for h in hexagon:
        if(h in a and a[h] not in s):
            s.append(a[h])
        elif(h in a and a[h] in s):
            return False
    return True


def check_is_valid(index, current_var, a, adjs, csp2):  #check if color is not equal to any of the neighbors
    adjacents_list = adjs[current_var]
    for adj in adjacents_list:
        if(adj in a.keys()):
            if(not check_thru_hex(csp2, adj, a)):
                return False
            if(index == a[adj]):
                return False

    return True

def select_var(a, v):   #a = assignment
    if(len(a) == 0):
        return 0
    for val in v.keys():
        if(val not in a):
            return val
    return 23

def create_vars():
    rs = {}
    for i in range(0,24):
        rs[i] = [1,2,3,4,5,6]
    return rs

def print_thing(a):
    print("  ", end='')
    for i in range(0, 5):
        print(a[i], end=' ')
    print("")
    for y in range(5, 12):
        print(a[y], end=' ')
    print("")
    for x in range(12, 19):
        print(a[x], end=' ')
    print("")
    print("  ",end='')
    for b in range(19,24):
        print(a[b], end=' ')
    print("")

vars = create_vars()
adjacents = {0: [1,6,7], 1:[0,6,7,2,8], 2:[1,7,8,9,3], 3:[2,8,9,10,4], 4:[3,9,10],
             5:[6,12,13], 6:[0,5,6,7,1], 7:[0,1,2,6,8,13,14,15], 8: [1,2,3,7,9,14,15,16], 9:[2,3,4,8,10,15,16,17],
             10: [3,4,9,11,16,17,18], 11:[10,17,18], 12:[5,6,13], 13:[5,6,7,12,14,19,20], 14:[6,7,8,13,15,19,20,21],
             15:[7,8,9,14,16,20,21,22], 16:[8,9,10,15,17,21,22,23], 17:[9,10,11,16,18,22,23], 18:[11,10,17,22,23],
             19:[13,14,20], 20:[13,14,15,19,21], 21:[14,15,16,20,22], 22:[15,16,17,21,23], 23:[16,17,18,22]}

hexagons = [[0,1,2,6,7,8],[2,3,4,8,9,10],[5,6,7,12,13,14],[7,8,9,14,15,16],[9,10,11,16,17,18],[13,14,15,19,20,21],
            [15,16,17,21,22,23]]   #second constraint

solution = backtrack_search(vars, adjacents, hexagons)
#print(solution)
print_thing(solution)





