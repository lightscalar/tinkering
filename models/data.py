import numpy as np
from tinkering.models.model import *
from tinkering.core.utils import *
from ipdb import set_trace as debug


def translate_to_bin(val, bins):
    """Translate a given value into a position in the given bin vector."""
    if estimate_data_type(bins) == "categorical":
        if val in bins:
            return np.where(np.array(bins) == val)[0][0]
        else:
            return None
    else:
        return np.argmin(np.abs(bins - val))


def find_counts(state, scope, models):
    """Find the number of counts associated with the specified state."""
    data = {}
    nb_elements = []

    # Grab the relevant data.
    for model in scope:
        data[model] = models[model].x_
        nb_elements.append(len(data[model]))

    if np.std(nb_elements) != 0:
        raise ValueError("All data sets must have the same number of elements.")

    for itr, model in enumerate(scope):
        if itr == 0:
            # This just initializes a vector of True values...
            boolean_matches = data[model] >= 0  # true for all values.

        # Now let's accumulate the matches. Kill off non-matches.
        boolean_matches = (data[model] == state[itr]) * boolean_matches

    return sum(boolean_matches)


class Data(Model):
    """The Data class."""

    def __init__(self, data):
        """Use DataMap class to adaptively histogram the data."""
        self.datamap = DataMap(data)
        self.x_ = self.datamap.x_
        self.counts = self.datamap.counts
        # self.x = x = np.array(data)
        # self.dtype = dtype = estimate_data_type(data)

        # if dtype == "categorical":
        #     self.bins = bins = sorted(set(x))
        #     self.counts = counts = np.array([sum(x == s) for s in bins])
        #     self.x_ = x_ = np.array([translate_to_bin(v, bins) for v in x])

        # elif dtype == "numeric":
        #     self.counts, self.bins = counts, bins = np.histogram(data, nb_bins)
        #     # self.counts = counts = self.counts[:-1]
        #     self.x_ = x_ = np.array([translate_to_bin(v, bins) for v in x])

        # Model specific things are done. Now add to the Universe.
        super(Data, self).__init__()

    @property
    def cardinality(self):
        # Cardinality is simply the number of elements in the domain -- in
        # other words, how many bins?
        return self.datamap.cardinality

    def _update_factor(self):
        """Called on initialization, and each time the network changes. If
        variable dependencies change, then we need to update the variable's
        factor, etc."""

        # If there are no dependencies, do this:
        if len(self.dependencies) == 0:
            # Find current cardinality, etc.
            scope = self.scope
            card = self.context.cardinalities
            self.factor = factor = Factor(scope, card)

            # Cycle through observed data. Adding unity to counts as a
            # Dirichlet prior.
            for bin_nb, counts in enumerate(self.counts):
                factor.set_phi([bin_nb], counts + 1)

            # Finish by normalizing.
            factor.normalize()
        else:
            # Now we have dependencies, so we must be a bit more clever.
            scope = self.scope
            cards = self.context.cardinalities
            models = self.context.models
            self.factor = factor = Factor(scope, cards)
            nb_states = factor.number_states
            for idx in np.arange(nb_states):
                print(f"{idx}/{nb_states}")
                assn = factor.get_assignment_from_index(idx)
                factor.set_phi(assn, 1 + find_counts(assn, scope, models))
