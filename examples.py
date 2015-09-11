from tinkering_beta.basics import *

# cardinality = {'cancer':2, 'tumor':2}
# f1 = Factor(['cancer', 'tumor'], cardinality)
# f1.set_phi([0, 0], 0.2)
# f1.set_phi([1, 0], 0.8)
# f1.set_phi([0, 1], 0.01)
# f1.set_phi([1, 1], 0.99)
# f2 = f1.marginalize('tumor')

tk = Tinkering()

# Build some models.
cold = tk.define('cold', Bool(0.2))
clouds = tk.define('clouds', Bool(0.5))
rain = tk.define('rain', Bool(0.2))

# Define relationship between variables.
rain.depends_on(clouds, cold)