import numpy as np
from pysat.formula import CNF , WCNF 
from pysat.pb import PBEnc
from pysat.card import CardEnc
from pysat.card import EncType
from pysat.solvers import Solver
import ssl
# print(ssl.OPENSSL_VERSION)



conference_sessions = 40
slots = 7
papers_range = np.arange(3, 7)  
max_parallel_sessions = 11 
working_groups = 20 
npMax = {1: 4, 2: 6, 3: 6, 4: 4, 5: 4, 6: 5, 7: 3} 

# list of groups session groups 
session_groups = [
    [1], [2], [3], [], [], [], [6], [7], [7, 8], [10], [8], [8, 11], [5, 8], 
    [3, 8], [7], [13], [13], [14], [], [13], [16], [16], [20], [17], [13], 
    [], [9], [11], [11, 12], [9], [6, 19], [], [], [18], [10], [5], [16], 
    [4, 5], [8, 12], [7, 15]
]


constraints = WCNF()

def get_number_of_papers_for_session():
    session_papers = {
        1: 14, 2: 23, 3: 12, 4: 9, 5: 9, 6: 6, 7: 10, 8: 4, 9: 10, 10: 7,
        11: 6, 12: 5, 13: 3, 14: 5, 15: 6, 16: 4, 17: 3, 18: 12, 19: 7, 20: 16,
        21: 4, 22: 5, 23: 14, 24: 11, 25: 4, 26: 3, 27: 10, 28: 6, 29: 6, 30: 4,
        31: 13, 32: 3, 33: 4, 34: 9, 35: 5, 36: 4, 37: 11, 38: 6, 39: 6, 40: 8
    }
    return session_papers

session_papers = get_number_of_papers_for_session()
np_s = session_papers[1]
# print(np_s)

def var_x(s, c, l):
    return (s-1)*slots * len(papers_range)  + (c-1)*len(papers_range) + l
    # can work with this code also
    # s_index = conference_sessions * slots * len(papers_range)
    # c_index = slots * len(papers_range)
    # l_index = len(papers_range)
    # return s_index - (conference_sessions - s) * c_index - (slots - c) * l_index - (len(papers_range) - l)
    
    

max_var_x = var_x(conference_sessions, slots, len(papers_range))

def var_z(s, c):
    z_offset = max_var_x + 1  # Start after the last x variable
    
  
    return z_offset + conference_sessions*slots - (conference_sessions-s)*slots - (slots - c)
    # work also with this 
    # return z_offset + (s - 1) * slots + c

max_var_z = var_z(conference_sessions, slots)
# fixed y problem 
def var_y(s1, s2, c, g):

    
    s1_index = conference_sessions* conference_sessions * slots * working_groups
    s2_index = conference_sessions * slots * working_groups
    c_index =  slots * working_groups
    g_index =  working_groups
    return s1_index - (conference_sessions - s1) * s2_index - (conference_sessions - s2) * c_index - (slots - c) * g_index - (g_index - g)

    
    # y_offset = max_var_z + 1

    # # Calculate the unique identifier for y variables
    # unique_index = ((s1 - 1) * conference_sessions + (s2 - 1)) * slots * working_groups + (c - 1) * working_groups + (g - 1) 
    # return y_offset + unique_index


# the first constraint
for s in range(1, conference_sessions + 1):
    for c in range(1, slots + 1):
        vars_for_s_c = [var_x(s, c, l) for l in papers_range]
        # Ensure that vars_for_s_c contains integers
        vars_for_s_c = [int(var) for var in vars_for_s_c]  # Convert all variables to integers
        amo_clause = CardEnc.atmost(lits=vars_for_s_c, bound=1, encoding=EncType.pairwise)
        constraints.extend(amo_clause.clauses)



# penser a
# the second constraint
for s in range(1, conference_sessions + 1):
    aux_vars = []  
    weights = []   

    for c in range(1, slots + 1):
        for l in papers_range:
            aux_vars.append(var_x(s, c, l))
            weights.append(l)  

   
    equals_clause = PBEnc.equals(lits=aux_vars, weights=weights, bound=session_papers[s])
    constraints.extend(equals_clause.clauses)

# print(constraints)

# 3 eme constraint

for s in range(1, conference_sessions + 1):
    for c in range(1, slots + 1):
        for l in papers_range:
            if l > npMax[c]:
               # j'ai travailler avec la conjunction des negation de x if l>npMax(c)
                constraints.append([-var_x(s, c, l)])




# Implementing the equivalence transformation
for s in range(1, conference_sessions + 1):
    for c in range(1, slots + 1):
        z_var = var_z(s, c)
        x_vars = [var_x(s, c, l) for l in papers_range]

        
        for x in x_vars:
            constraints.append([-z_var, -x])
            # modified 
        or_clause = [x for x in x_vars] + [z_var]
        constraints.append(or_clause)


## code added


# The Fourth constraint
for c in range(1, slots + 1):
    neg_z_vars = [-var_z(s, c) for s in range(1, conference_sessions + 1)]
    # Convert all variables in neg_z_vars to integers
    neg_z_vars = [int(var) for var in neg_z_vars]
    # Ensure max_parallel_sessions is an integer
    max_parallel_sessions_int = int(max_parallel_sessions)
    atmost_clause = CardEnc.atmost(lits=neg_z_vars, bound=max_parallel_sessions_int, encoding=EncType.seqcounter)
    constraints.extend(atmost_clause.clauses)



# write this to file // remember this 

y_var = 0#last varliable + x+y
## here soft constraints
for s1 in range(1, conference_sessions + 1):
    for s2 in range(s1 + 1, conference_sessions + 1):  # Ensure s1 < s2
        for c in range(1, slots + 1):
            common_groups = set(session_groups[s1 - 1]).intersection(session_groups[s2 - 1])
            for g in common_groups:
                #y_var = var_y(s1, s2, c, g)
                y_var = y_var + 1
                constraints.append([-y_var], weight=1)
                ### hard contranint 
                constraints.append([var_z(s1,c),var_z(s2,c),var_y])
                ###
# Implementing the conflict treatment constraint
for s1 in range(1, conference_sessions + 1):
    for s2 in range(s1 + 1, conference_sessions + 1):  # Ensure s1 < s2
        for c in range(1, slots + 1):
            common_groups = set(session_groups[s1 - 1]).intersection(session_groups[s2 - 1])
            for g in common_groups:
                # Generate the y variable for the conflict
                y_var = var_y(s1, s2, c, g)

                
                neg_x_s1_clauses = [-var_x(s1, c, l) for l in papers_range]
                neg_x_s2_clauses = [-var_x(s2, c, l) for l in papers_range]

                for x_var in neg_x_s1_clauses + neg_x_s2_clauses:
                    constraints.append([x_var, y_var])



for i in range (1,5):
    constraints.append(var_z(34,i))

constraints.to_file('output.cnf')
# add thursday constraint 
# decodage de var_x
# add constraitn z(34,[1,2,3])