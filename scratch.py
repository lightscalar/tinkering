from numpy import *
from tinkering.basics import *


# Play around.
tk = Tinkering()
define = tk.define

# Now create some models.
pop = 1000
gender_data = []
height_data = []
for k in arange(pop):
    if random.rand() > 0.5:
        gender_data.append('male')
        height_data.append(6 + 0.1*random.randn())
    else:
        gender_data.append('female')
        height_data.append(5+0.2*random.randn())

# Define the gender and height random variables.
gender = define('gender', Data(gender_data))
height = define('height', Data(height_data))


# height.depends_on(gender)
