from pysat.formula import CNF
from pysat.solvers import Solver

# Define the problem
cnf = CNF()

# Adding clauses (using numbers to represent variables)
# Let's say Alice = 1, Bob = 2, Carol = 3, Dave = 4
cnf.append([-1, -2])  # -1 represents not Alice, so this is ¬Alice ∨ ¬Bob
cnf.append([-2, -3])  # ¬Bob ∨ ¬Carol
cnf.append([-3, 4])   # ¬Carol ∨ Dave
cnf.append([1, 4])    # Alice ∨ Dave

# Write to a CNF file
cnf.to_file('party_problem.cnf')
