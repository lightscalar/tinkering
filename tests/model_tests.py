from tinkering.basics import *
from nose.tools import assert_equals, assert_almost_equals, assert_raises
from nose import with_setup
from numpy.testing import assert_array_almost_equal_nulp, assert_array_equal


def setup():
    global tk, define
    tk = Tinkering()
    define = tk.define


def teardown():
    pass


def starts_with_no_dependencies_test():
    smoker = tk.define('smoker', Bool(0.01))
    assert_equals(smoker.dependencies, [])


@with_setup(setup, teardown)
def add_dependencies_test():
    smoker = tk.define('smoker', Bool(0.1))
    cancer_gene = tk.define('cancer_gene', Bool(0.05))
    cancer = tk.define('cancer', Bool(0.1))
    cancer.depends_on(smoker, cancer_gene, smoker)

    # We added the dependencies. There were no duplicates.
    assert_equals('smoker' in cancer.dependencies, True)
    assert_equals('cancer_gene' in cancer.dependencies, True)
    assert_equals(len(cancer.dependencies), 2)


def ingest_numeric_data_test():
    temps = [65.2, 78.2, 90.3]
    data = define('height', Data(temps))
    assert_equals(data.dtype, 'numeric')
    assert_equals(len(data.bins), 26)
    assert_equals(sum(data.counts), 3)
    assert_equals(data._dependencies, [])
    assert_equals(data.factor.phi.shape, (26,))


def ingest_categorical_data_test():
    temps = ['cat', 'kitten', 'anteater', 'barbie', 'xenomorph', 'crayfish']
    srtd =  ['anteater', 'barbie', 'cat', 'crayfish', 'kitten', 'xenomorph']
    data = define('animal', Data(temps))
    assert_equals(data.dtype, 'categorical')
    assert_equals(data.bins, srtd)
    assert_array_equal(data.counts, [1,1,1,1,1,1])
    assert_equals(data._dependencies, [])
    assert_equals(data.factor.phi.shape, (6,))



