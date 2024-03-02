from pysat.examples.rc2 import RC2
from pysat.formula import WCNF


wcnf = WCNF(from_file='output.cnf')


with RC2(wcnf) as solver:
    is_sat = solver.compute()

    if is_sat:
       
        model = solver.model
        
        print("Solution:", model)
    else:
        print("No solution found")


