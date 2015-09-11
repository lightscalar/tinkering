from model import *


class Bool(Model):

    def __init__(self, probability_of_true):
        self.model_type = 'boolean'
        self.domain = [False, True]
        self.probability_of_true = probability_of_true
        self.generate_factor()

    def generate_factor(self):
        # Generate a factor for this random variable.

    @property
    def cardinality(self):
        # Cardinality is simply the number of elements in the domain.
        return len(self.domain)


# Let's alias Flip to Bool for convenience
Flip = Bool
