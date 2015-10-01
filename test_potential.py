import numpy as np
from potential import Potential
#

pot_x1 = Potential([0], np.array([2]), np.array([0.9, 0.1]))
pot_x2 = Potential([1], np.array([2]), np.array([1.0, 1.0]))

pot_x2x1 = Potential([1, 0], np.array([2, 2]), np.array([[0.9, 0.2], [0.1, 0.8]]))
pot_x1x2 = Potential([0, 1], np.array([2, 2]), np.array([[0.9, 0.1], [0.2, 0.8]]))

pot_m12_x2 = Potential([1], np.array([2]), np.array([0.83, 0.17]))

res1 = pot_x2x1.multiply(pot_x1)

res1_ver = Potential([1, 0], np.array([2, 2]), np.array([[0.81, 0.02], [0.09, 0.08]]))
print res1
assert res1 == res1_ver

res2 = pot_x1x2.multiply(pot_x1)
res2_ver = Potential([0, 1], np.array([2, 2]), np.array([[0.81, 0.09], [0.02, 0.08]]))
print res2
assert res2 == res2_ver

res3 = pot_x2.multiply(pot_m12_x2)
res3_ver = Potential([1], np.array([2]), np.array([0.83, 0.17]))
assert res3 == res3_ver
print res3

res4 = pot_x1.multiply(pot_x1x2, True)
print 'res4'
print res4
assert res4 == res2

pot_mar1 = res1.marginalize([1])
print pot_mar1
pot_mar2 = res2.marginalize([1])
print pot_mar2
print pot_m12_x2
assert pot_mar1 == pot_m12_x2
assert pot_mar2 == pot_m12_x2
