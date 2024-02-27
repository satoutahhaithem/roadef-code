from pysat.solvers import Solver
from pysat.formula import WCNF

# Load the WCNF file
wcnf = WCNF(from_file='output.cnf')

# Initialize the solver, for example, using Glucose4
with Solver(name='g4', with_proof=True) as solver:

    # Add all clauses from the WCNF to the solver
    solver.append_formula(wcnf)

    # Solve the problem
    if solver.solve():
        model = solver.get_model()
        print("Solution:", model)
    else:
        print("No solution found")
