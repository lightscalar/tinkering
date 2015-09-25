from tinkering.basics import *
from nose.tools import assert_equals, assert_almost_equals, assert_raises
from nose import with_setup
from numpy.testing import assert_array_almost_equal_nulp, assert_array_equal
import numpy as np


def setup():
    global tk, scope, cardinalities, factor
    tk = Tinkering()
    scope = ['fever', 'cold', 'cancer']
    cardinalities = {'cancer': 2, 'cold': 3, 'fever': 3}
    factor = Factor(scope, cardinalities)


def teardown():
    pass


# BEGIN TESTS ------------------------------------------------------
@with_setup(setup, teardown)
def test_scope_ordering():
    assert_array_equal(factor.scope, ['cancer', 'cold', 'fever'])


@with_setup(setup, teardown)
def test_cardinality_dict():
    assert_equals(factor.cardinalities, {'cancer': 2, 'cold': 3, 'fever': 3})


@with_setup(setup, teardown)
def test_cardinality_list():
    assert_array_equal(factor.cardinality_list, np.array([2,3,3]))


@with_setup(setup, teardown)
def test_number_states_computation():
    assert_equals(factor.number_states, 18)


@with_setup(setup, teardown)
def test_number_states_computation():
    assert_array_equal(factor.phi, np.zeros(18))


@with_setup(setup, teardown)
def test_stride_length_calculations_1():
    assert_array_equal(factor.stride, np.array([1,2,6]))


def test_stride_length_calculations_2():
    scope = ['cancer', 'cold']
    cardinalities = {'cancer': 2, 'cold': 2}
    f = Factor(scope, cardinalities)
    assert_array_equal(f.stride, np.array([1,2]))


def test_stride_length_calculations_3():
    scope = ['cancer', 'cold', 'fever', 'drunk']
    cardinalities = {'cancer': 2, 'cold': 2, 'fever': 4, 'drunk': 3}
    f = Factor(scope, cardinalities)
    assert_array_equal(f.stride, np.array([1,2,4,12]))


def test_get_assignment():
    scope = [0,1]
    cardinalities = {0: 2, 1: 2}
    f = Factor(scope, cardinalities)
    assert_array_equal(f.get_assignment_from_index(0), [0,0])


def test_index_and_assignment():
    scope = ['fever', 'cold', 'cancer']
    scope = ['cancer', 'cold', 'fever', 'drunk']
    cardinalities = {'cancer': 2, 'cold': 2, 'fever': 4, 'drunk': 3}
    f = Factor(scope, cardinalities)

    # Ensure all indices generate assignments that
    # translate back to the correct index.
    for idx in range(f.number_states):
        assn = f.get_assignment_from_index(idx)
        new_idx = f.get_index_from_assignment(assn)
        assert_equals(new_idx, idx)


def test_set_phi():
    scope = ['cold', 'cancer']
    cardinalities = {'cancer': 2, 'cold': 2, 'fever': 4, 'drunk': 3}
    f = Factor(scope, cardinalities)
    f.set_phi([1,0], 0.2)
    assert_equals(f.get_phi([1,0]), 0.2)


def test_reduce_removes_models_from_scope():
    scope = ['fever', 'cold', 'cancer']
    scope = ['cancer', 'cold', 'fever', 'drunk']
    cardinalities = {'cancer': 2, 'cold': 2, 'fever': 4, 'drunk': 3}
    f = Factor(scope, cardinalities)
    g = f.reduce('cancer', 0)
    assert_array_equal(g.scope, ['cold', 'drunk', 'fever'])


def test_reduction_is_correct():
    scope = [0, 1, 2]
    cardinalities = {0:2, 1:2, 2:2}
    f = Factor(scope, cardinalities)
    f.set_phi([0, 0, 0], 0.2)
    f.set_phi([1, 0, 0], 0.8)
    f.set_phi([0, 1, 0], 0.2)
    f.set_phi([1, 1, 0], 0.5)
    f.set_phi([0, 0, 1], 0.)
    f.set_phi([1, 0, 1], 0.9)
    f.set_phi([0, 1, 1], 0.3)
    f.set_phi([1, 1, 1], 0.7)
    g = f.reduce(1, 1)
    assert_array_almost_equal_nulp(g.scope, np.array([0,2]))
    assert_array_almost_equal_nulp(g.phi, np.array([0.2, 0.5, 0.3, 0.7]))


def test_reduction_is_correct_2():
    scope = [0, 1]
    cardinalities = {0:2, 1:2, 2:2}
    f = Factor(scope, cardinalities)
    f.set_phi([0, 0], 0.2)
    f.set_phi([1, 0], 0.8)
    f.set_phi([0, 1], 0.2)
    f.set_phi([1, 1], 0.5)
    g = f.reduce(0, 1)
    assert_array_almost_equal_nulp(g.scope, np.array([1]))
    assert_array_almost_equal_nulp(g.phi, np.array([0.8, 0.5]))
    m = f.reduce(1,0)
    assert_array_almost_equal_nulp(m.phi, np.array([0.2, 0.8]))


def test_reduction_to_unit_factor():
    scope = [0, 1, 2]
    cardinalities = {0:2, 1:2, 2:2}
    f = Factor(scope, cardinalities)
    f.set_phi([0, 0, 0], 0.2)
    f.set_phi([1, 0, 0], 0.8)
    f.set_phi([0, 1, 0], 0.2)
    f.set_phi([1, 1, 0], 0.5)
    f.set_phi([0, 0, 1], 0.)
    f.set_phi([1, 0, 1], 0.9)
    f.set_phi([0, 1, 1], 0.3)
    f.set_phi([1, 1, 1], 0.7)
    g = f.reduce(1, 1)
    h = g.reduce(0, 0)
    m = h.reduce(2, 1)
    assert_equals(f.is_unit_factor, False)
    assert_equals(g.is_unit_factor, False)
    assert_equals(h.is_unit_factor, False)
    assert_equals(m.is_unit_factor, True)


def test_unit_factor_product():
    cardinalities = {0:2, 1:2, 2:2}
    f = Factor([], cardinalities)
    g = Factor([1], cardinalities)
    assert_equals(f.is_unit_factor, True)
    assert_equals(g.is_unit_factor, False)
    assert_equals(f.product(g), g)
    assert_equals(g.product(f), g)


def test_scope_of_product():
    cardinality = {'cancer':2, 'tumor':2}
    f1 = Factor(['cancer', 'tumor'], cardinality)
    f1.set_phi([0, 0], 0.2)
    f1.set_phi([1, 0], 0.8)
    f1.set_phi([0, 1], 0.01)
    f1.set_phi([1, 1], 0.99)
    f2 = Factor(['cancer'], cardinality)
    f2.set_phi([0], 0.8)
    f2.set_phi([1], 0.2)
    f3 = f1.product(f2)
    assert_array_equal(f3.scope, ['cancer', 'tumor'])


def test_product_between_two_factors():
    cardinality = {'cancer':2, 'tumor':2}
    f1 = Factor(['cancer', 'tumor'], cardinality)
    f1.set_phi([0, 0], 0.2)
    f1.set_phi([1, 0], 0.8)
    f1.set_phi([0, 1], 0.01)
    f1.set_phi([1, 1], 0.99)
    f2 = Factor(['cancer'], cardinality)
    f2.set_phi([0], 0.8)
    f2.set_phi([1], 0.2)
    f3 = f1.product(f2)
    assert_array_equal(f3.scope, ['cancer', 'tumor'])


def test_product_between_two_factors():
    cardinality = {'cancer':2, 'tumor':2}
    f1 = Factor(['cancer', 'tumor'], cardinality)
    f1.set_phi([0, 0], 0.2)
    f1.set_phi([1, 0], 0.8)
    f1.set_phi([0, 1], 0.01)
    f1.set_phi([1, 1], 0.99)
    f2 = Factor(['tumor'], cardinality)
    f2.set_phi([0], 0.8)
    f2.set_phi([1], 0.2)
    f3 = f1.product(f2)
    assert_array_almost_equal_nulp(f3.phi, [ 0.16 ,  0.64 ,  0.002,  0.198])


def test_commutativity_with_operator_overloading():
    cardinality = {'cancer':2, 'tumor':2}
    f1 = Factor(['cancer', 'tumor'], cardinality)
    f1.set_phi([0, 0], 0.2)
    f1.set_phi([1, 0], 0.8)
    f1.set_phi([0, 1], 0.01)
    f1.set_phi([1, 1], 0.99)
    f2 = Factor(['tumor'], cardinality)
    f2.set_phi([0], 0.8)
    f2.set_phi([1], 0.2)
    f3 = f1 * f2
    f4 = f2 * f1
    assert_array_almost_equal_nulp(f3.phi, [ 0.16 ,  0.64 ,  0.002,  0.198])
    assert_array_almost_equal_nulp(f4.phi, [ 0.16 ,  0.64 ,  0.002,  0.198])


def test_marginalized_factor_removes_model():
    cardinality = {'cancer':2, 'tumor':2}
    f1 = Factor(['cancer', 'tumor'], cardinality)
    f1.set_phi([0, 0], 0.2)
    f1.set_phi([1, 0], 0.8)
    f1.set_phi([0, 1], 0.01)
    f1.set_phi([1, 1], 0.99)
    f2 = f1.marginalize('tumor')
    assert_array_equal(f2.scope, ['cancer'])


def test_marginalized_phi_is_correct():
    cardinality = {'cancer':2, 'tumor':2}
    f1 = Factor(['cancer', 'tumor'], cardinality)
    f1.set_phi([0, 0], 0.2)
    f1.set_phi([1, 0], 0.8)
    f1.set_phi([0, 1], 0.01)
    f1.set_phi([1, 1], 0.99)
    f2 = f1.marginalize('tumor')
    f3 = f1.marginalize('cancer')
    assert_array_almost_equal_nulp(f2.phi, [0.21, 1.79])
    assert_array_almost_equal_nulp(f3.phi, [1, 1])


