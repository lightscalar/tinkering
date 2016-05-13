from tinkering.basics import *
from nose.tools import assert_equals, assert_almost_equals
from nose import with_setup
from numpy.testing import assert_array_almost_equal_nulp, assert_array_equal


def setup():
    global heads, tails
    heads = Bool(0.5)
    tails = Flip(0.5)


def teardown():
    pass


# BEGIN TESTS ------------------------------------------------------
@with_setup(setup, teardown)
def test_create_bool():
    assert_equals(heads.probability_of_true, 0.5)
    assert_equals(tails.probability_of_true, 0.5)


@with_setup(setup, teardown)
def test_bins():
    assert_equals(heads.bins, [False, True])
    assert_equals(tails.bins, [False, True])


@with_setup(setup, teardown)
def test_cardinality():
    assert_equals(heads.cardinality, 2)
    assert_equals(tails.cardinality, 2)



# @with_setup(setup, teardown)
# def
# tk.define('cancer', Flip(0.2))
