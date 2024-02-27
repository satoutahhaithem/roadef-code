from pysat.formula import CNF
from pysat.solvers import Solver


cnf = CNF()


cnf.append([-1, -2])  
cnf.append([-2, -3])  
cnf.append([-3, 4])  
cnf.append([1, 4])    

# Write to a CNF file
cnf.to_file('exampleSolver.cnf')
