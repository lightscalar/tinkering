"""Utility functions for processing numerical data."""
import numpy as np
from ipdb import set_trace as debug


class DataMap:
    """Maps data from discrete integers to original values, and vice versa."""

    def __init__(self, data_samples):
        self.is_numeric = is_numeric(data_samples[0])
        if self.is_numeric:
            self.is_discrete = is_discrete(data_samples)
        self.data_samples = np.array(data_samples)
        self.discretize()

    def discretize(self):
        """Discretize the data samples."""
        if self.is_numeric:
            if self.is_discrete:
                # Build maps between discrete labels and values.
                unique_vals = sorted(np.unique(self.data_samples))
                self.data_to_label = {v: k for k, v in enumerate(unique_vals)}
                self.label_to_data = {k: v for k, v in enumerate(unique_vals)}
                self.cardinality = len(unique_vals)
                self.x_ = self.convert_data_to_label(self.data_samples)
                self.counts = np.array(
                    [np.sum(self.data_samples == val) for val in unique_vals]
                )
            else:
                # Adaptive histogram.
                self.data_bins = bayesian_blocks(self.data_samples)
                self.data_bins = np.hstack((-np.inf, self.data_bins))
                hist_bins = np.hstack((self.data_bins, np.inf))
                self.counts, _ = np.histogram(self.data_samples, bins=hist_bins)
                self.x_ = self.convert_data_to_label(self.data_samples)
                self.label_to_data = breakpoints_to_vals(self.data_bins)
                self.cardinality = len(self.data_bins)
        else:
            # Data is categorical... enumerate the categories!
            unique_vals = sorted(np.unique(self.data_samples))
            self.data_to_label = {v: k for k, v in enumerate(unique_vals)}
            self.label_to_data = {k: v for k, v in enumerate(unique_vals)}
            self.cardinality = len(unique_vals)
            self.x_ = self.convert_data_to_label(self.data_samples)
            self.counts = np.array(
                [np.sum(self.data_samples == val) for val in unique_vals]
            )
            self.x_ = np.array(self.x_)

    def convert_data_to_label(self, data):
        """Convert raw data to discrete label."""
        if self.is_numeric and not self.is_discrete:
            # Data is numerical, so look for change points in binning...
            labels = [np.max(np.where(d > self.data_bins)) for d in data]
        else:
            # Data is intrinsically discrete.
            labels = [self.data_to_label[d] for d in data]
        return labels

    def convert_label_to_data(self, labels):
        """Convert discrete label to data (approx)."""
        data = [self.label_to_data[l] for l in labels]
        return data


def is_numeric(value):
    """Determine if a value is numeric."""
    try:
        float(value)
        return True
    except:
        return False


def estimate_data_type(data_samples):
    """Characterize the data's type. Will return either :categorical or
       :numeric."""
    for sample in data_samples:
        if not is_numeric(sample):
            return "categorical"
    return "numeric"


def is_discrete(data_samples, threshold=25):
    """Determine if numerical data is discrete or continuous."""
    unique_vals = np.unique(data_samples)
    return len(unique_vals) < threshold


def breakpoints_to_vals(breakpoints):
    """Convert a list of breakpoints to values for label to number conversion."""
    breaks = breakpoints[1:]
    mean_diff = np.mean(np.diff(breaks))
    vals = [breaks[0] - mean_diff / 2]
    for k in range(0, len(breaks) - 1):
        vals.append((breaks[k] + breaks[k + 1]) / 2)
    vals.append(breaks[-1] + mean_diff / 2)
    return np.array(vals)


def bayesian_blocks(t):
    """Bayesian Blocks Implementation

    Parameters
    ----------
    t : ndarray, length N
        data to be histogrammed

    Returns
    -------
    bins : ndarray
        array containing the (N+1) bin edges

    """
    # copy and sort the array
    t = np.sort(t)
    N = t.size

    # create length-(N + 1) array of cell edges
    edges = np.concatenate([t[:1], 0.5 * (t[1:] + t[:-1]), t[-1:]])
    block_length = t[-1] - edges

    # arrays needed for the iteration
    nn_vec = np.ones(N)
    best = np.zeros(N, dtype=float)
    last = np.zeros(N, dtype=int)

    # -----------------------------------------------------------------
    # Start with first data cell; add one cell at each iteration
    # -----------------------------------------------------------------
    for K in range(N):
        # Compute the width and count of the final bin for all possible
        # locations of the K^th changepoint
        width = block_length[: K + 1] - block_length[K + 1]
        count_vec = np.cumsum(nn_vec[: K + 1][::-1])[::-1]

        # evaluate fitness function for these possibilities
        fit_vec = count_vec * (np.log(count_vec) - np.log(width))
        fit_vec -= 4  # 4 comes from the prior on the number of changepoints
        fit_vec[1:] += best[:K]

        # find the max of the fitness: this is the K^th changepoint
        i_max = np.argmax(fit_vec)
        last[K] = i_max
        best[K] = fit_vec[i_max]

    # -----------------------------------------------------------------
    # Recover changepoints by iteratively peeling off the last block
    # -----------------------------------------------------------------
    change_points = np.zeros(N, dtype=int)
    i_cp = N
    ind = N
    while True:
        i_cp -= 1
        change_points[i_cp] = ind
        if ind == 0:
            break
        ind = last[ind - 1]
    change_points = change_points[i_cp:]
    return edges[change_points]


if __name__ == "__main__":

    data = np.random.randn(500)
    d = DataMap(data)

    cats_data = ["male", "male", "female", "male", "female"]
    cats = DataMap(cats_data)
