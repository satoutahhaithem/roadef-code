import numpy as np
from pysat.formula import *
from pysat.pb import EncType as pbenc
from pysat.pb import *
from pysat.card import *
from pysat.solvers import *
import ssl
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
# print(ssl.OPENSSL_VERSION)



conference_sessions = 40
slots = 7
papers_range = [3,4,5,6]
max_parallel_sessions = 11
working_groups = 20 
np= [14,23,12,9,9,6,10,4,10,7,6,5,3,5,6,4,3,12,7,16,4,5,14,11,4,3,10,6,6,4,13,3,4,9,5,4,11,6,6,8]
npMax = [4, 6, 6, 4, 4, 5,  3]
session_groups = [
    [1], [2], [3], [], [], [], [6], [7], [7, 8], [10], [8], [8, 11], [5, 8], 
    [3, 8], [7], [13], [13], [14], [], [13], [16], [16], [20], [17], [13], 
    [], [9], [11], [11, 12], [9], [6, 19], [], [], [18], [10], [5], [16], 
    [4, 5], [8, 12], [7, 15]
]
# conference_sessions = 2
# slots = 3
# papers_range = [3,4]
# max_parallel_sessions = 2
# working_groups = 2
# np = [3,4]
# npMax = [4, 6, 6, 4, 4, 5,  3]
# session_groups = [
#     [1,2], [2,1]
# ]
# list of groups session groups 


constraints = WCNF()

# def get_number_of_papers_for_session():
#     session_papers = {
#         1: 14, 2: 23, 3: 12, 4: 9, 5: 9, 6: 6, 7: 10, 8: 4, 9: 10, 10: 7,
#         11: 6, 12: 5, 13: 3, 14: 5, 15: 6, 16: 4, 17: 3, 18: 12, 19: 7, 20: 16,
#         21: 4, 22: 5, 23: 14, 24: 11, 25: 4, 26: 3, 27: 10, 28: 6, 29: 6, 30: 4,
#         31: 13, 32: 3, 33: 4, 34: 9, 35: 5, 36: 4, 37: 11, 38: 6, 39: 6, 40: 8
#     }
#     return session_papers

# session_papers = get_number_of_papers_for_session()
# np_s = session_papers[1]
# print(np_s)

def var_x(s, c, l):
    return (s-1)*slots * len(papers_range)  + (c-1)*len(papers_range) + l
    # can work with this code also
    # s_index = conference_sessions * slots * len(papers_range)
    # c_index = slots * len(papers_range)
    # l_index = len(papers_range)
    # return s_index - (conference_sessions - s) * c_index - (slots - c) * l_index - (len(papers_range) - l)
    
    

# function to decode var_x
def decode_var_x(x, slots, papers_range_length):
    x -= 1  # Adjusting because the original function seems 1-indexed
    l = x % papers_range_length + 1
    x //= papers_range_length
    c = x % slots + 1
    s = x // slots + 1
    return s, c, l

def var_z(s, c):
    max_var_x = var_x(conference_sessions, slots, len(papers_range))    
  
    # return max_var_x + conference_sessions*slots - (conference_sessions-s)*slots - (slots - c)
    # work also with this 
    return max_var_x + (s - 1) * slots + c

max_var_z = var_z(conference_sessions, slots)
# fixed y problem 
# def var_y(s1, s2, c, g):

    
#     s1_index = conference_sessions* conference_sessions * slots * working_groups
#     s2_index = conference_sessions * slots * working_groups
#     c_index =  slots * working_groups
#     g_index =  working_groups
#     return s1_index - (conference_sessions - s1) * s2_index - (conference_sessions - s2) * c_index - (slots - c) * g_index - (g_index - g)

    
    # y_offset = max_var_z + 1

    # # Calculate the unique identifier for y variables
    # unique_index = ((s1 - 1) * conference_sessions + (s2 - 1)) * slots * working_groups + (c - 1) * working_groups + (g - 1) 
    # return y_offset + unique_index

y_var = var_z(conference_sessions,slots)    #last varliable + x+y


# # the first constraint
for s in range(1, conference_sessions + 1):
    for c in range(1, slots + 1):
        vars_for_s_c = []
        for l in range(1,len(papers_range)+1):
        # i modify paper range to len(paperRange) , 
            vars_for_s_c.append(var_x(s, c, l))
            # Ensure that vars_for_s_c contains integers
            #add global varibale here EncType.pairwise
        amo_clause = CardEnc.atmost(lits=vars_for_s_c, bound=1, top_id=y_var,encoding=EncType.cardnetwrk) 
        y_var=amo_clause.nv
        constraints.extend(amo_clause.clauses)






# penser a
# the second constraint
for s in range(1, conference_sessions +1):
    aux_vars = []  
    for c in range(1,slots + 1):
        for l in range(1,len(papers_range)+1):
            for i in range(papers_range[l-1]):
                aux_vars.append(var_x(s, c, l))
            # print ("THe aux var var ", aux_vars)

            #weights.append(papers_range[l-1])  
            # print ("the weights ", weights)

    
    eq_clause = CardEnc.equals(lits=aux_vars, bound=np[s-1], top_id=y_var, encoding=EncType.cardnetwrk)
    #equals_clause = PBEnc.equals(lits=aux_vars, weights=weights,bound=np[s-1], top_id=max_var_z, encoding= pbenc.best)
    # equals_clause = PBEnc.atleast(lits=aux_vars, weights=weights,bound=np[s-1], top_id=max_var_z, encoding= pbenc.best)
    y_var=eq_clause.nv
    constraints.extend(eq_clause.clauses)




# # print(constraints)

# 3 eme constraint

for s in range(1, conference_sessions + 1):
    for c in range(1, slots + 1):
        for l in range(1,len(papers_range)+1):
            if papers_range[l-1] > npMax[c-1]:
               # j'ai travailler avec la conjunction des negation de x if l>npMax(c)
                constraints.append([-var_x(s, c, l)])


# The Fourth constraint
for c in range(1, slots + 1):
    neg_z_vars = []
    for s in range(1, conference_sessions + 1):
        neg_z_vars.append(-var_z(s, c))
    # Convert all variables in neg_z_vars to integers
    ## verify this int () cause 
    # Ensure max_parallel_sessions is an integer
    ## do global variable 
    atmost_clause = CardEnc.atmost(lits=neg_z_vars, bound=max_parallel_sessions, top_id=y_var, encoding=EncType.cardnetwrk)
    y_var=atmost_clause.nv
    constraints.extend(atmost_clause.clauses)



# Implementing the equivalence transformation
for s in range(1, conference_sessions + 1):
    for c in range(1, slots + 1):
        z_var = var_z(s, c)
        x_vars=[]
        for l in range(1,len(papers_range)+1):
            x_vars.append(var_x(s, c, l))
        or_clause = x_vars + [z_var]
        constraints.append(or_clause)

        for x in x_vars:
            constraints.append([-z_var, -x])
            # modified 


## code added



# write this to file // remember this 
# i add this also for the offset
## here soft constraints
for s1 in range(1, conference_sessions + 1):
    for s2 in range(s1 + 1, conference_sessions + 1):  # Ensure s1 < s2
        common_groups = set(session_groups[s1 - 1]).intersection(session_groups[s2 - 1])
        for c in range(1, slots + 1):
            for g in common_groups:
                #y_var = var_y(s1, s2, c, g)
                y_var = y_var + 1
                constraints.append([-y_var], weight=1)
                ### hard contranint of conflict treatment 
                constraints.append([var_z(s1,c),var_z(s2,c),y_var])
                ###


# constraint for 34 session
for i in range (1,5):
    constraints.append([var_z(34,i)])


constraints.to_file("file.cnf")




# Assuming other parts of your code (constraint definitions, SAT model setup) are correctly implemented

def display_assignments_by_slot_with_counts(model, slots, papers_range, conference_sessions):
    slot_assignments = {c: {} for c in range(1, slots + 1)}  # Initialize dictionaries for each slot

    # Processing the model to populate slot assignments
    for var in model:
        if var > 0:
            s, c, l = decode_var_x(var, slots, len(papers_range))
            paper_count = papers_range[l - 1]
            if s not in slot_assignments[c]:
                slot_assignments[c][s] = paper_count
            else:
                slot_assignments[c][s] += paper_count  # Accumulate paper count for the session

    
    total_sessions_displayed = 0
    for slot in sorted(slot_assignments):
        print(f"Slot {slot}:")
        sessions_in_slot = 0
        for session, count in sorted(slot_assignments[slot].items()):
            if sessions_in_slot < max_parallel_sessions and total_sessions_displayed < 77:
                print(f"  Conference Session {session} with {count} papers")
                sessions_in_slot += 1
                total_sessions_displayed += 1
            else:
                break  # Stop if the slot or total limit is reached
def detect_conflicts(model, slots, conference_sessions, session_groups):
    # Initialize a dictionary to store the groups associated with each session in each slot
    slot_group_sessions = {c: {} for c in range(1, slots + 1)}

    # Populate the dictionary based on the model's assignments
    for var in model:
        if var > 0:
            s, c, _ = decode_var_x(var, slots, len(papers_range))
            for g in session_groups[s - 1]:
                if g not in slot_group_sessions[c]:
                    slot_group_sessions[c][g] = [s]
                else:
                    slot_group_sessions[c][g].append(s)

    # Detect conflicts
    conflicts = []
    for c, groups in slot_group_sessions.items():
        for g, sessions in groups.items():
            if len(sessions) > 1:
                conflicts.append((c, g, sessions))

    return conflicts

# Function to display conflicts
def display_conflicts(conflicts):
    if conflicts:
        print("Conflicts detected:")
        for slot, group, sessions in conflicts:
            print(f"Conflict in slot {slot} for group {group} in sessions {', '.join(map(str, sessions))}")
    else:
        print("No conflicts detected.")

with RC2(constraints, solver="Cadical153") as solver:
    for model in solver.enumerate():
        print('Model has cost:', solver.cost)
        display_assignments_by_slot_with_counts(model, slots, papers_range, conference_sessions)
        break  # Process only the first model


    # verfier mlih 

# add thursday constraint 
# decodage de var_x
# rename the len(paperrange) in variable
# try with rc2 solver 
# read this https://pysathq.github.io/docs/html/api/examples/rc2.html
# write script tp generate the new formule a
# test rc2
# look at the new variant
# second constraint do it with encodage pseudo boolean 
# do it with excel 
# solver essay avec maxcdcdl 
#decodage 


# from pysat.examples.fm import FM

# # wcnf = WCNF(from_file='file.cnf')
# fm = FM(constraints, verbose=0)
# fm.compute()  # set of hard clauses should be satisfiable
# print(fm.cost) # cost of MaxSAT solution should be 2
# # print(fm.model)
import pandas as pd

# Assuming you have a function that returns the model results in a structured format:
# Example format: [{'slot': 1, 'session': 1, 'papers': 4}, {'slot': 1, 'session': 2, 'papers': 5}, ...]
def get_model_results():
    # This function should return the results from your model.
    # For now, it's just an example placeholder.
    return [{'slot': 1, 'session': 1, 'papers': 4}, {'slot': 1, 'session': 2, 'papers': 5}]

# Convert the results to a pandas DataFrame
results = get_model_results()
df = pd.DataFrame(results)

# Writing DataFrame to an Excel file
excel_path = './file.xlsx'  # Replace with your file path
df.to_excel(excel_path, index=False)

print(f"Results have been written to {excel_path}")
