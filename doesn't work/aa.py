import numpy as np
import itertools
from pysat.formula import CNF
from pysat.solvers import Solver

# Define problem parameters
conference_sessions = np.arange(1, 41)  # 40 sessions
slots = np.arange(1, 10)  # 9 slots across 3 days
papers_range = np.arange(3, 7)  # 3-6 papers per session
max_parallel_sessions = 11  # Up to 11 sessions can be held in parallel
working_groups = np.arange(1, 21)  # 20 working groups

# Define session to working group associations (example)
# This should be based on your actual data
session_to_wg = {
    1: [1], 2: [2], 3: [3], 4: [], 5: [], 6: [], 7: [6],
    8: [7], 9: [7, 8], 10: [10], 11: [8], 12: [8, 11],
    13: [5, 8], 14: [3, 8], 15: [7], 16: [13], 17: [13],
    18: [14], 19: [], 20: [13], 21: [16], 22: [16],
    23: [20], 24: [17], 25: [13], 26: [], 27: [9],
    28: [11], 29: [11, 12], 30: [9], 31: [6, 19], 32: [],
    33: [], 34: [18], 35: [10], 36: [5], 37: [16],
    38: [4, 5], 39: [8, 12], 40: [7, 15]
}

session_time_slots = {
    1: 1.33,  # 11h to 12h20
    2: 2.00,  # 14h to 16h
    3: 2.00,  # 16h30 to 18h30
    4: 1.33,  # 17h10 to 18h30 (overlap with slot 3)
    5: 1.33,  # 10h45 to 12h05
    6: 1.00,  # 14h45 to 15h45
    7: 1.33,  # 10h45 to 12h20
    8: 1.67,  # 14h to 15h40
    9: 1.33,  # 16h10 to 17h30
}
# Calculate maximum number of papers per slot
max_papers_per_slot = {slot: int(duration * 60 / 20) for slot, duration in session_time_slots.items()}

# Map variables for SAT solver
var_counter = 1
var_map = {}
conflict_map = {}
for session in conference_sessions:
    for slot in slots:
        for papers in papers_range:
            var_map[(session, slot, papers)] = var_counter
            var_counter += 1
    for group in working_groups:
        # This will map each session and working group to a unique variable
        conflict_map[(session, group)] = var_counter
        var_counter += 1

# Initialize CNF formula
cnf = CNF()

import itertools

# Add constraints for session uniqueness
for session in conference_sessions:
    for papers in papers_range:
        cnf.append([var_map[(session, slot, papers)] for slot in slots])
        for slot1, slot2 in itertools.combinations(slots, 2):
            cnf.append([-var_map[(session, slot1, papers)], -var_map[(session, slot2, papers)]])

# Add constraints for even distribution across slots
for slot in slots:
    target_sessions_per_slot = len(conference_sessions) // len(slots)
    for papers in papers_range:
        session_combinations = itertools.combinations(conference_sessions, target_sessions_per_slot + 1)
        for combination in session_combinations:
            clause = [-var_map[(session, slot, papers)] for session in combination]
            cnf.append(clause)

# Add constraints to ensure that the number of papers in each slot does not exceed the maximum
for slot in slots:
    for session_combination in itertools.combinations(conference_sessions, max_parallel_sessions + 1):
        for papers in papers_range:
            max_papers = max_papers_per_slot[slot]
            clause = [-var_map[(session, slot, papers)] for session in session_combination]
            if sum(papers for session in session_combination) > max_papers:
                cnf.append(clause)

# # Add constraints to ensure a maximum of 11 sessions in parallel for each slot
# for slot in slots:
#     for session_combination in itertools.combinations(conference_sessions, max_parallel_sessions + 1):
#         clause = [-var_map[(session, slot, papers)] for session in session_combination for papers in papers_range]
#         cnf.append(clause)

# Add additional constraints for conflict management based on working groups
for group in working_groups:
    for s1, s2 in itertools.combinations(conference_sessions, 2):
        if group in session_to_wg.get(s1, []) and group in session_to_wg.get(s2, []):
            for slot in slots:
                cnf.append([-conflict_map[(s1, group)], -conflict_map[(s2, group)]])


# Additional constraints for conflict management
for group in working_groups:
    for s1, s2 in itertools.combinations(conference_sessions, 2):
        if group in session_to_wg.get(s1, []) and group in session_to_wg.get(s2, []):
            for slot in slots:
                # Add constraint that these two sessions cannot be in the same slot
                cnf.append([-var_map[(s1, slot, papers)], -var_map[(s2, slot, papers)]])

# Solve CNF formula
solver = Solver()
solver.append_formula(cnf)

if solver.solve():
    model = solver.get_model()
    # Process and print the model
    for session in conference_sessions:
        for slot in slots:
            for papers in papers_range:
                if var_map[(session, slot, papers)] in model:
                    print(f'Session {session} is in slot {slot} with {papers} papers')
    # Check for any conflicts
    conflicts = []
    for group in working_groups:
        for session1, session2 in itertools.combinations(conference_sessions, 2):
            if conflict_map[(session1, group)] in model and conflict_map[(session2, group)] in model:
                conflicts.append((session1, session2, group))
    if conflicts:
        print("Conflicts detected:")
        for session1, session2, group in conflicts:
            print(f'Sessions {session1} and {session2} have a conflict in Group {group}')
else:
    print('No solution found')

