
import numpy as np
from pysat.formula import CNF
from pysat.solvers import Solver

# Define the problem parameters based on the ROADEF challenge
conference_sessions = np.arange(1, 41)  # 40 sessions
slots = np.arange(1, 8)  # 7 slots
papers_range = np.arange(3, 7)  # 3 to 6 papers per session
max_parallel_sessions = 11  # Max parallel sessions per slot

# Mapping variables to integers for SAT solver
var_counter = 1
var_map = {}
for session in conference_sessions:
    for slot in slots:
        for papers in papers_range:
            var_map[(session, slot, papers)] = var_counter
            var_counter += 1

# Initialize CNF formula
cnf = CNF()

# Constraints to ensure sessions are evenly distributed across slots
for session in conference_sessions:
    # Each session must be assigned to only one slot
    session_clauses = [var_map[(session, slot, papers)] for slot in slots for papers in papers_range]
    cnf.append(session_clauses)

    # Pairwise negation to ensure uniqueness
    for i in range(len(session_clauses)):
        for j in range(i + 1, len(session_clauses)):
            cnf.append([-session_clauses[i], -session_clauses[j]])

# Additional constraints to ensure sessions are distributed across all slots
for slot in slots:
    slot_clauses = []
    for session in conference_sessions:
        slot_clauses += [var_map[(session, slot, papers)] for papers in papers_range]
    # At least one session must be assigned to each slot
    cnf.append(slot_clauses)

# Solve the CNF formula
solver = Solver()
solver.append_formula(cnf)
if solver.solve():
    model = solver.get_model()
    # Interpret the solution
    for session in conference_sessions:
        for slot in slots:
            for papers in papers_range:
                if var_map[(session, slot, papers)] in model:
                    print(f'Session {session} is in slot {slot} with {papers} papers')
else:
    print('No solution found')

# Note: Logic for minimizing working group conflicts can be added based on specific requirements
