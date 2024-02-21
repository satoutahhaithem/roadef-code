from pysat.formula import CNF
import csv

# Define your variables and constants
num_sessions = 40
num_slots = 7
num_paper_amounts = 4  # Assuming L = {3, 4, 5, 6}

# Maximum number of papers for each slot
max_papers_per_slot = {
    1: 4,
    2: 6,
    3: 6,
    4: 4,
    5: 4,
    6: 5,
    7: 3
}

# Create a CNF formula
formula = CNF()

# Constraint: Each session is assigned to exactly one slot and one paper amount
for s in range(1, num_sessions + 1):
    for c in range(1, num_slots + 1):
        clause = [f'x_{s}_{c}_{l}' for l in range(1, num_paper_amounts + 1)]
        clause = [int(l.replace('x_', '').split('_')[2]) for l in clause]  # Convert variable names to integers
        formula.append(clause)
        for literal in clause:
            formula.append([literal])  # Remove weight parameter

        # Add a constraint to ensure only one paper amount is selected for each session and slot
        formula.append(clause)

# Constraint: Total number of papers assigned to a session in a slot doesn't exceed the maximum allowed for that slot
for s in range(1, num_sessions + 1):
    for c in range(1, num_slots + 1):
        for l in range(1, num_paper_amounts + 1):
            # Add a clause ensuring the session isn't assigned more papers than allowed in the slot
            if l > max_papers_per_slot[c]:
                formula.append([-int(f'x_{s}_{c}_{l}'.replace('x_', '').split('_')[2])])  # Convert variable name to integer

# Constraint: Each slot must have at least one session
for c in range(1, num_slots + 1):
    clause = [f'x_{s}_{c}_{l}' for s in range(1, num_sessions + 1) for l in range(1, num_paper_amounts + 1)]
    clause = [int(l.replace('x_', '').split('_')[2]) for l in clause]  # Convert variable names to integers
    formula.append(clause)  # Remove weight parameter

# Export to CSV file
with open('cnf_formula.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for clause in formula.clauses:
        writer.writerow(clause)
