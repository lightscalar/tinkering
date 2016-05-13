from model import *


class Bool(Model):

    def __init__(self, probability_of_true):
        self.model_type = 'boolean'
        self.bins = [False, True]
        self.probability_of_true = probability_of_true
        super(Bool,self).__init__()

    def __repr__(self):
        return '{%s | Bool(%.2f)}' % (self.id, self.probability_of_true)

    def _update_factor(self):
        pass

    def generate_factor(self):
        # Generate a factor for this random variable.
        # self.factor = Factor()
        pass

    @property
    def cardinality(self):
        # Cardinality is simply the number of elements in the domain.
        return len(self.bins)


# Let's alias Flip to Bool for convenience
Flip = Bool
