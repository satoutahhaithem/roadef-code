import numpy as np
from pysat.formula import CNF
from pysat.solvers import Solver

# Define problem parameters
conference_sessions = np.arange(1, 41)  # 40 sessions
slots = np.arange(1, 10)  # 9 slots across 3 days
papers_range = np.arange(3, 7)  # 3-6 papers per session
max_parallel_sessions = 11  # Up to 11 sessions can be held in parallel
working_groups = np.arange(1,21)
# Session time slots (in hours), calculated based on the provided schedule
# The key is the slot number, and the value is the duration of the slot
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

# Calculate the maximum number of papers per slot, given that each paper takes 20 minutes
max_papers_per_slot = {slot: int(duration * 60 / 20) for slot, duration in session_time_slots.items()}

# Map variables to integers for SAT solver
var_counter = 1
var_map = {}
conflict_map = {}
for session in conference_sessions:
    for slot in slots:
        for papers in papers_range:
            var_map[(session, slot, papers)] = var_counter
            var_counter += 1

# Initialize CNF formula
cnf = CNF()

import itertools

# Constraints for session uniqueness
for session in conference_sessions:
    # For each session, create a clause that the session must take place in exactly one slot with a specific number of papers
    for papers in papers_range:
        # Each session and paper combination should appear in exactly one slot
        cnf.append([var_map[(session, slot, papers)] for slot in slots])

        # Add clauses to ensure that a session does not appear in more than one slot for the same number of papers
        for slot1, slot2 in itertools.combinations(slots, 2):
            cnf.append([-var_map[(session, slot1, papers)], -var_map[(session, slot2, papers)]])

# Constraints for even distribution across slots
for slot in slots:
    # For each slot, we want to distribute the sessions as evenly as possible
    # This means that if we have 40 sessions and 9 slots, each slot should have about 40/9 sessions
    target_sessions_per_slot = len(conference_sessions) // len(slots)
    for papers in papers_range:
        # Create combinations of sessions such that there are not more than the target number of sessions per slot
        session_combinations = itertools.combinations(conference_sessions, target_sessions_per_slot + 1)
        for combination in session_combinations:
            clause = [-var_map[(session, slot, papers)] for session in combination]
            cnf.append(clause)

# ... (Rest of the code)

# Don't forget to add the solver logic to solve the CNF and handle the output


# Constraints to ensure that the number of papers in each slot does not exceed the maximum
for slot in slots:
    # For each slot, create a clause that limits the number of papers to the maximum allowed
    for session_combination in itertools.combinations(conference_sessions, max_parallel_sessions + 1):
        for papers in papers_range:
            # If the slot duration allows for a certain number of papers, then we cannot have more sessions than that
            # running in parallel that exceed the number of papers that can be presented.
            max_papers = max_papers_per_slot[slot]  # This should be the total number of papers that can be presented in the slot
            # Generate clauses for each combination of sessions that exceed the paper limit
            clause = [-var_map[(session, slot, papers)] for session in session_combination]
            # Only add this clause if the combination of papers exceeds the maximum allowed in the slot
            if sum(papers for session in session_combination) > max_papers:
                cnf.append(clause)


# Add additional constraints to ensure that a maximum of 11 sessions can be scheduled in parallel for each slot
for slot in slots:
    # Create all possible combinations of 12 sessions, since we can have a maximum of 11 parallel sessions
    for session_combination in itertools.combinations(conference_sessions, max_parallel_sessions + 1):
        # For each combination of 12, create a clause that at least one session is not in the current slot
        clause = [-var_map[(session, slot, papers)] for session in session_combination for papers in papers_range]
        cnf.append(clause)

# Additional constraints for conflict management
for group in working_groups:
    for slot in slots:
        for session1, session2 in itertools.combinations(conference_sessions, 2):
            # Add a constraint that if session1 and session2 involve the same working group,
            # they cannot be scheduled in the same slot.
            cnf.append([-conflict_map[(session1, group)], -conflict_map[(session2, group)]])


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
    for group in range(1, 21):  # Assuming 20 working groups
        for session1, session2 in itertools.combinations(conference_sessions, 2):
            if conflict_map[(session1, group)] in model and conflict_map[(session2, group)] in model:
                conflicts.append((session1, session2, group))
    if conflicts:
        print("Conflicts detected:")
        for session1, session2, group in conflicts:
            print(f'Sessions {session1} and {session2} have a conflict in Group {group}')
else:
    print('No solution found')
