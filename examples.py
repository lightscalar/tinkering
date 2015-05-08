from tinkering_beta.basics import *

scope = [0, 1]
cardinalities = {0:2, 1:2, 2:2}
f = Factor(scope, cardinalities)
f.set_phi([0, 0], 0.2)
f.set_phi([1, 0], 0.8)
f.set_phi([0, 1], 0.2)
f.set_phi([1, 1], 0.5)
# g = f.reduce(0, 1)
m = f.reduce(1,0)
# assert_array_almost_equal_nulp(m.phi, np.array([0.2, 0.8]))
# assert_array_almost_equal_nulp(g.scope, np.array([0,1]))
# assert_array_almost_equal_nulp(g.phi, np.array([0.8, 0.5]))