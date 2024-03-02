from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

# Step 1: Load the WCNF file
wcnf = WCNF(from_file='output.cnf')
print(wcnf)
with RC2(wcnf) as rc2:
    for m in rc2.enumerate():
        print('model {0} has cost {1}'.format(m, rc2.cost))




