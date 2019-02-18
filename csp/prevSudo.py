#Alexis Echano

from time import time
import collections

class CSP:

    def __init__(self, variables: object, domains: object, neighbors: object, num) -> object:
        # a list of variables
        self.variables = variables

        # a dict of {variable:[a list of possible values]}
        self.domains = domains
        # a dict of {variables:[a list of variables]
        self.neighbors = neighbors
        self.initial = ()
        self.curr_domains = None

    def assign(self, var, val, assignment):
        assignment[var] = val
        # self.update_neighbor_domains(var, assignment)

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
            # self.update_neighbor_domains(var, assignment)

    def support_pruning(self):
        """Make sure we can prune values from domains. """
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

def forward_checking(csp, var, value, assignment, removals, num):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for i in range(num):
        for B in csp.neighbors[var][i]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if value == b:
                        csp.prune(B, b, removals)
                if not csp.curr_domains[B]:
                    return False
    return True


def mrv_unassigned_variable(assignment, csp, num):

    csp.domains = build_domains(csp.variables, assignment, csp.neighbors, num)
    unassigned = {}
    for key in csp.domains:
        if key not in assignment:
            unassigned[key] = len(csp.domains[key])

    return min(unassigned, key=unassigned.get)

def check_for_single_occurances(var, value, assignment, csp, num):
    for i in range(num):
        for neighbor in csp.neighbors[var][i]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
    return True

def is_consistent(var, value, assignment, csp, num):
    if len(assignment) == 0:
        return True
    return check_for_single_occurances(var, value, assignment, csp, num)

def backtracking_search(csp, assignment, num, select_unassigned_variable=mrv_unassigned_variable, checker=forward_checking):

    def backtrack(assignment, num):
        if len(assignment) == len(csp.variables):
            return assignment

        var = select_unassigned_variable(assignment, csp, num)

        for value in csp.domains[var]:

            if is_consistent(var, value, assignment, csp, num):

                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)

                if(checker(csp, var, value, assignment, removals, num)):
                    result = backtrack(assignment, num)
                    if(result != None):
                        return result
                csp.restore(removals)

        csp.unassign(var, assignment)
        return None

    result = backtrack(assignment, num)

    return result


def build_grid(inputstr, num):
    grid = []
    indexes = num * num
    for i in range(1, indexes+1):
        rowstr = inputstr[(i-1)*indexes: i*indexes]
        row = []
        for j in range(indexes):
            row.append(rowstr[j])
        grid.append(row)

    return grid


def build_variables(num):
    vars = []

    indexes = num*num
    for r in range(indexes):
        for c in range(indexes):
            vars.append(str(r) + str(c))
    return vars

def build_domains(variables, assignment, neighbors, num):
    domains = {}

    # get unique values in row, col, 3x3 --> determine possibilities
    for var in variables:   #FOR EVERY INDEX P MUCH
        used_vals = set()
        for i in range(num):  #for every row, col and box
            for neighbor in neighbors[var][i]:  #for each neighbor
                 if neighbor in assignment: #if its already in assignment
                    used_vals.add( assignment[neighbor] )

        if(num == 3):
            temp_set = set([1,2,3,4,5,6,7,8,9])
        if(num == 4):
            temp_set = set(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G'])

        values = set(temp_set - used_vals)
        domains[var] = values


    # if a value is not allowed in any other cells in the row or col or 3x3, then this value is the only possible value for var
    for i in range(num):
        for var in variables:
            for val in domains[var]:
                if len(domains[var]) > 1:
                    count = 0
                    for neighbor in neighbors[var][i]:
                        if val not in domains[neighbor]:
                            count += 1
                    if count == 8:
                        domains[var] = [val]
                        break
    return domains


def buildrowcolumnneighbors(var, num):

    row = set()
    col = set()
    rindex = var[0]
    cindex = var[1]

    indexes = num*num

    for i in range(indexes):
        if i != int(cindex):
            row.add(rindex + str(i))
        if i != int(rindex):
            col.add(str(i) + cindex)

    return row, col

def buildboxneighbors(var, single_num):

    start_row = int(var[0]) // single_num
    start_col = int(var[1]) // single_num

    start_row = start_row*single_num
    start_col = start_col*single_num

    neighbors = set([str(i) + str(j) for i in range(start_row, start_row + single_num) for j in range(start_col, start_col + single_num)])
    #neighbors.remove(var)
    return neighbors

def buildneighbors(variables, num):
    neighbors = {}
    for var in variables:
        rowcol = buildrowcolumnneighbors(var, num)
        neighbors[var] = (rowcol[0], rowcol[1], buildboxneighbors(var, num))

    return neighbors

def initassignments(vars, grid):

    assignments = {}
    for v in vars:
        if grid[int(v[0])][int(v[1])] != '.':
            assignments[v] = int(grid[int(v[0])][int(v[1])])

    return assignments

def checkSum(pzl):  #correctness is 405
    sum = 0
    for i in pzl.keys():
        sum += ord(str(pzl[i]))
    return sum - (48*81)

def print_str_checksum(assignment):
    od = collections.OrderedDict(sorted(assignment.items()))
    str1 = ''.join(str(e)for e in od.values())
    #val = checkSum(assignment)
    str1 = "[" + str1 + ", "  + "]"#str(val)+ "]"
    print(str1)

def detect_type(firstLine):
    if(len(firstLine) == 81):
        return 3
    if(len(firstLine) == 256):
        return 4

def main_method():
    file = input("Enter filename: ").lower()
    file_contents = open(file, 'r').read().split()
    puz_num = 1

    the_num = detect_type(file_contents[0])
    variables = build_variables(the_num)
    neighbors = buildneighbors(variables, the_num)

    total_time = time()

    while (len(file_contents) > 0):
        grid = build_grid(str(file_contents.pop(0)), the_num)
        assignments = initassignments(variables, grid)

        csp = CSP(variables, {}, neighbors, the_num)

        t = time()  # begins time
        result = backtracking_search(csp, assignments, the_num, select_unassigned_variable=mrv_unassigned_variable, checker=forward_checking)

        print("- - - - - - - - - -")
        print("Puzzle #" + str(puz_num), end=' ')
        print_str_checksum(result)
        print('Time: ' + str(time() - t))  # ends time
        print("Total Time: " + str(time() - total_time))  # total time elapsed

        puz_num += 1

main_method()