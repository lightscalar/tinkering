from tinkering_beta.basics import *

cardinality = {'cancer':2, 'tumor':2}
f1 = Factor(['cancer','tumor'], cardinality)
f1.set_phi([0, 0], 0.2)
f1.set_phi([1, 0], 0.8)
f1.set_phi([0, 1], 0.01)
f1.set_phi([1, 1], 0.99)
f2 = Factor(['tumor'], cardinality)
f2.set_phi([0], 0.8)
f2.set_phi([1], 0.2)
f3 = f1.product(f2)

scope = ['fever', 'cold', 'cancer']
cardinalities = {'cancer': 2, 'cold': 3, 'fever': 3}
factor = Factor(scope, cardinalities)