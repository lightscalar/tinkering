from tinkering.basics import *


# Play around.
tk = Tinkering()

# Now create some models.
cancer = tk.define('cancer', Bool(0.4))
smoker = tk.define('smoker', Bool(0.2))
cancer_gene = tk.define('cancer_gene', Bool(0.02))

cancer.depends_on(smoker, cancer_gene)
