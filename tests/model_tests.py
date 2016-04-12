from tinkering.basics import *
from nose.tools import assert_equals, assert_almost_equals, assert_raises
from nose import with_setup
from numpy.testing import assert_array_almost_equal_nulp, assert_array_equal


def setup():
    global tk
    tk = Tinkering()


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
