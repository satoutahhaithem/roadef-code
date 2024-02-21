import numpy as np
from pysat.formula import CNF
from pysat.solvers import Solver

# Define problem parameters
conference_sessions = np.arange(1, 41)
slots = np.arange(1, 8)
papers_range = np.arange(3, 7)
max_parallel_sessions = 11
working_groups = np.arange(1, 21)

# Map variables to integers for SAT solver
var_counter = 1
var_map = {}
conflict_map = {}
for session in conference_sessions:
    for slot in slots:
        for papers in papers_range:
            var_map[(session, slot, papers)] = var_counter
            var_counter += 1
    for group in working_groups:
        conflict_map[(session, group)] = var_counter
        var_counter += 1

# Initialize CNF formula
cnf = CNF()

# Constraints for even distribution and uniqueness
for session in conference_sessions:
    session_clauses = [var_map[(session, slot, papers)] for slot in slots for papers in papers_range]
    cnf.append(session_clauses)
    for i in range(len(session_clauses)):
        for j in range(i + 1, len(session_clauses)):
            cnf.append([-session_clauses[i], -session_clauses[j]])

# Additional constraints for conflict management
for group in working_groups:
    for s1 in conference_sessions:
        for s2 in conference_sessions:
            if s1 < s2:
                for slot in slots:
                    for l1 in papers_range:
                        for l2 in papers_range:
                            cnf.append([-var_map[(s1, slot, l1)], -var_map[(s2, slot, l2)], conflict_map[(s1, group)]])
                            cnf.append([-var_map[(s1, slot, l1)], -var_map[(s2, slot, l2)], conflict_map[(s2, group)]])

# Solve CNF formula
solver = Solver()
solver.append_formula(cnf)
if solver.solve():
    model = solver.get_model()
    conflicts = []
    for session in conference_sessions:
        for slot in slots:
            for papers in papers_range:
                if var_map[(session, slot, papers)] in model:
                    print(f'Session {session} is in slot {slot} with {papers} papers')
        for group in working_groups:
            if conflict_map[(session, group)] in model:
                conflicts.append((session, group))
    if conflicts:
        print("Conflicts detected. Sessions and groups with conflicts:")
        for session, group in conflicts:
            print(f'Session {session}, Group {group}')
else:
    print('No solution found')
