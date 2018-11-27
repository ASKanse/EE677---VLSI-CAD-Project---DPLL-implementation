global assignments
global unit_count
global tree_split_count

def reduce(pos, literal): #put the value of litral in the pos 
    reduced = list()  #remove the litral from all the clauses after assigning a value to it
    if literal[0] == '!':
        comp_lit = literal[1] # when the litral is assigned false value
    else:
        comp_lit = '!'+literal # when the litral is assigned true value
    for clause in pos:
        if comp_lit in clause:  # if opposite literal in clause, remove just literal
            temp = []
            for lit in clause:       
                if lit != comp_lit:  
                    temp.append(lit)  
            reduced.append(temp)
        elif literal not in clause:  # if literal in clause, remove clause
            reduced.append(clause)
    return reduced

def dpll(pos):
    # sat check
    if len(pos) == 0:  # if list is empty then sat => all the clauses are satisfied
        return "SAT"
    if [] in pos: # if an empty list present in pos then unsat => one of the clauses has all the value zero
        return "UNSAT"

    # unit clause-propagation
    for clause in pos:
        if len(clause) == 1:  # check if it is unit-clause
            if clause[0][0] == '!': 
                assignments[clause[0][1]] = 'false' # if unit clause in complemented form
            else:
                assignments[clause[0]] = 'true'  # if unit clause in uncomplemented form
            temp = reduce(pos, clause[0])
            unit_count += 1
            return dpll(temp)  #recurse 

    # assigning an unassigned literal true or false and checking for sat if no unit clause present
    tree_split_count += 1
    for literal in assignments:
        if assignments[literal] == 0:  # if not assigned given value of 0
            traceback_asgn = {}
            for k in assignments:
                traceback_asgn[k] = assignments[k] # for tracing back to original table if we get un sat alog a path
            assignments[literal] = 'false'
            temp1 = dpll(reduce(pos, '!' + literal)) # dpll on subtree of literal = 1
            if temp1 == 'SAT':
                return 'SAT'
            else:
                assignments = traceback_asgn  
                assignments[literal] = 'true'
                temp2 = dpll(reduce(pos, literal)) # dpll on subtree of literal = 0
                return temp2

if __name__ == "__main__":
    unit_count = 0
    tree_split_count = 0
    POS = []
    literal_set = set() # storeduced the list of literals
    assignments = {}
    ip_file = input("Input file name:")

    input_file = open(ip_file, 'r')
    clause =input_ ilef.readline()
    while clause: 
        temp = clause.rstrip().split(' ')
        for c in temp:
            if c[0] == '!':
                literal_set.add(c[1])
            else:
                literal_set.add(c)
        POS.append(temp)
        clause = input_file.readline()
    for literal in literal_set:
        assignments[literal] = 0
    input_file.close()

    dpll_out = dpll(POS)
    print(dpll_out)
    if dpll_out == 'SAT':
        assignments = sorted(assignments.items())
        for val in assignments:
            if val[1] != 0:
                print(val[0], "=", val[1])

    print("Unit propagation count:", unit_count)
    print("Splitting count:", tree_split_count)