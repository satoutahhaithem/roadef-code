import numpy as np
from pysat.formula import CNF , WCNF
from pysat.card import CardEnc
from pysat.card import EncType
from pysat.solvers import Solver


conference_sessions = 40
slots = 7
papers_range = np.arange(3, 7)  
max_parallel_sessions = 11 
working_groups = 20 
npMax = {1: 4, 2: 6, 3: 6, 4: 4, 5: 4, 6: 5, 7: 3} 
session_time_slots = {
    1: 1.33,  
    2: 2.00,  
    3: 2.00,  
    4: 1.33,  
    5: 1.33,  
    6: 1.00,  
    7: 1.33,   
}
hard_constraints = CNF()
soft_constraints = WCNF()

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
print(np_s)

def var_x(s, c, l):
    s_index = conference_sessions * slots * len(papers_range)
    c_index = slots * len(papers_range)
    l_index = len(papers_range)
    return int(s_index - (conference_sessions - s) * c_index - (slots - c) * l_index - (papers_range[-1] - l)) ## twalah dima int madirshash type np.arrange



max_var_x = var_x(conference_sessions, slots, papers_range[-1])


def var_y(s1, s2, c, g):
    s1_index = conference_sessions**2 * slots * working_groups
    s2_index = conference_sessions * slots * working_groups
    c_index = slots * working_groups
    g_index = working_groups
    offset = max_var_x + 1 
    return offset + s1_index - (conference_sessions - s1)**2 * s2_index - (conference_sessions - s2) * c_index - (slots - c) * g_index - (working_groups - g)

# hadi constraint lowla
for s in range(1, conference_sessions + 1):
    aux_vars = [] # bah t3awan bih
    for c in range(1, slots + 1):
        for l in papers_range:
            aux_vars.extend([var_x(s, c, l)] * l)

    equals_clause = CardEnc.equals(lits=aux_vars, bound=np(s))
    hard_constraints.extend(equals_clause.clauses)
