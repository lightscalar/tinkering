from model import *


class Bool(Model):

    def __init__(self, probability_of_true):
        super(Bool,self).__init__()
        self.model_type = 'boolean'
        self.domain = [False, True]
        self.probability_of_true = probability_of_true
        self.generate_factor()


    def __repr__(self):
        return '{%s | Bool(%.2f)}' % (self.id, self.probability_of_true)

    def generate_factor(self):
        # Generate a factor for this random variable.
        # self.factor = Factor()
        pass

    @property
    def cardinality(self):
        # Cardinality is simply the number of elements in the domain.
        return len(self.domain)


# Let's alias Flip to Bool for convenience
Flip = Bool
