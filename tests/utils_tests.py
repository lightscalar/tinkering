from tinkering.basics import *
from nose.tools import assert_equals, assert_almost_equals, assert_raises
from nose import with_setup
from numpy.testing import assert_array_almost_equal_nulp, assert_array_equal


def setup():
    global tk
    tk = Tinkering()


def teardown():
    pass


def is_numeric_test():
    assert_equals(is_numeric(4), True)
    assert_equals(is_numeric('Matthew'), False)


def estimate_data_type_test():
    assert_equals(estimate_data_type([1,2,3,4,5]), 'numeric')
    assert_equals(estimate_data_type(['hot', 'cold', 'hot']), 'categorical')
