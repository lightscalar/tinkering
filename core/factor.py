'''Factors for making efficient probabilistic inference in Bayesian networks.

    DESCRIPTION
    ---
    Suppose we have random variables A, B, C, ..., that can take values Val(A), Val(B), ...
    A factor is simply a mapping from the values of a collection of random variables to the
    real line: i.e.,

           Factor(A, B, C): Val(A,B,C) --> Positive Real Line

    We can perform various operations on factors -- multiplying them, marginalizing them over
    certain variables, etc.

    It will be common for us to represent conditional probability distributions as factors. for
    example, if we have a simple Bayesian network with two variables A and B, then P(A|B)P(B)
    is the factor defining the network. We can represent it as the product of two factors
            H1(A,B) = P(A|B)
    together with,
            H2(B) = P(B)
    Then we can simply compute,
            H3(A,B) = H1 * H2
    And we are guaranteed that the multiplication occurs in the correct manner. Similarly, if we
    are ultimately interested in the probability distribution over one variable or another, we
    can marginalize:
            P(A) = H3(A,B).marginalize(B); or,
            P(B) = H3(A,B).marginalize(A); etc
'''
import numpy as np
import pdb


class Factor:

    def __init__(self, scope, cardinalities):
        self.scope = sorted(scope)
        self.number_models = len(self.scope)
        self.is_unit_factor = self.number_models == 0
        self.cardinalities = cardinalities
        self.cardinality_list = np.array([self.cardinalities[key] for key in self.scope])
        self.number_states = np.prod([self.cardinalities[key] for key in scope])
        self.phi = np.zeros(self.number_states)
        self.set_strides()

    def set_strides(self):
        # Set the strides associated with in-scope models.
        if self.is_unit_factor:
            self.stride = np.array([])
        else:
            stride = np.zeros(self.number_models, dtype=int)
            stride[0] = 1
            for idx,model in enumerate(self.scope[0:-1]):
                stride[idx+1] = self.cardinalities[model] * stride[idx]
            self.stride = stride

    def get_assignment_from_index(self, index):
        # Return the assignment corresponding to a given index into PHI.
        return (np.floor(index/self.stride) % self.cardinality_list).astype(int)

    def get_index_from_assignment(self, assignment):
        # Get the index corresponding to a particular assignment.
        return np.sum(np.dot(assignment, self.stride)).astype(int)

    def set_phi(self, assignment, value):
        # Set phi for a given assignment to the specified value.
        idx = self.get_index_from_assignment(assignment)
        self.phi[idx] = value

    def get_phi(self, assignment):
        # Set phi for a given assignment to the specified value.
        idx = self.get_index_from_assignment(assignment)
        return self.phi[idx]

    def reduce(self, model_id, model_value):
        # Reduce the factor by setting the specified model to its specified value.
        model_index = self.scope.index(model_id)
        cardinality = self.cardinalities[model_id]

        # Remove target model from the scope. Create a new factor.
        updated_scope = [mdl for mdl in self.scope if mdl != model_id]
        reduced_factor = Factor(updated_scope, self.cardinalities)

        # Check to see if it is a unit factor.
        if reduced_factor.is_unit_factor:
            return reduced_factor

        # Find indices corresponding to specified model having specified value.
        stride = self.stride[model_index]
        values = np.floor(np.arange(self.number_states)/stride) % cardinality
        target_indices = np.nonzero(values == model_value)[0]
        reduced_factor.phi = self.phi[target_indices]
        return reduced_factor

    def product(self, other_factor):
        # Computes the product between this factor and another one.

        # If None is passed in, just return the current factor.
        if not other_factor:
            return self

        # Taking product with unit factor returns self.
        if self.is_unit_factor:
            return other_factor
        elif other_factor.is_unit_factor:
            return self

        # Okay. We got ourselves a genYOUine product here.
        # INSERT MAGICK HERE.





