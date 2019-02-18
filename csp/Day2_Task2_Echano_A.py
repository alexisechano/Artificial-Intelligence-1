#Name: Alexis Echano    #Date: 11/9/2018

#Task 2: In Class Lab - Austrailia

def backtrack_search(vars, csp):
    return backtrack_search_helper(vars, {} ,csp)

def backtrack_search_helper(vars, assignment, csp):
    if(check_if_done(assignment, csp, len(vars))):
        return assignment

    var = select_var(assignment, vars)
    for color in vars[var]: #the colors

        if(check_is_valid(color, var, assignment, vars, csp)):
            assignment[var] = color
            result = backtrack_search_helper(vars, assignment, csp)
            if(result != None):
                return result
            assignment.pop(var)
    return None

def check_if_done(current, csp, lenVar):
    if(len(current) != lenVar):
        return False
    for key in current:
        if(key == "T"):
            continue
        for stuff in csp[key]:
            if(current[stuff] == current[key]):
                return False
    return True

def check_is_valid(color, current_var, a, v, adjs):  #check if color is not equal to any of the neighbors
    adjacents_list = adjs[current_var]
    for adj in adjacents_list:
        if(adj in a.keys()):
            if(color == a[adj]):
                return False
    return True

def select_var(a, v):   #a = assignment
    if(len(a) == 0):
        return "WA"
    for val in v.keys():
        if(val not in a):
            return val
    return "T"

def foolproof_check(dict):  #just to double check
    check = {"WA": "R", "NT": "G", "SA": "B", "Q": "R", "NSW": "G", "V": "R", "T": "R"}
    for k in dict.keys():
        if(dict[k] != check[k]):
            return False
    return True


vars = {"WA": ['R', 'G', 'B'], "SA": ['R', 'G', 'B'], "NT": ['R', 'G', 'B'], "Q": ['R', 'G', 'B'], "NSW": ['R', 'G', 'B'], "V": ['R', 'G', 'B'], "T": ['R', 'G', 'B']}
adjacents = {"WA": ["NT", "SA"], "SA": ["WA", "NT", "Q", "NSW", "V"], "NT": ["WA", "SA", "Q"], "Q": ["NT", "SA", "NSW"], "NSW": ["SA",  "Q", "V"], "V": ["SA", "NSW"], "T": ['']}

solution = backtrack_search(vars, adjacents)
print(solution)

#print(foolproof_check(solution)) #double check



