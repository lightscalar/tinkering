from tinkering.basics import *
from nose.tools import assert_equals, assert_almost_equals, assert_raises
from nose import with_setup
from numpy.testing import assert_array_almost_equal_nulp, assert_array_equal


def setup():
    global tk
    tk = Tinkering()


def teardown():
    pass


# BEGIN TESTS ------------------------------------------------------
@with_setup(setup, teardown)
def test_create_tinkering_object():
    assert_equals(tk.number_models,0)


@with_setup(setup, teardown)
def test_create_tinkering_object():
    assert_equals(tk.model_ids, [])


@with_setup(setup, teardown)
def test_no_network_present():
    assert_equals(tk.network, {})


@with_setup(setup, teardown)
def test_models_are_dicts():
    assert_equals(type(tk.models), dict)


@with_setup(setup, teardown)
def test_define_model():
    cancer = tk.define('cancer', Bool(0.1))
    assert_equals(tk.number_models, 1)


@with_setup(setup, teardown)
def test_context_present():
    cancer = tk.define('cancer', Bool(0.1))
    assert_equals(cancer.context.number_models, 1)
    cold = tk.define('cold', Flip(0.3))
    assert_equals(cold.context.number_models, 2)


@with_setup(setup, teardown)
def test_model_has_id():
    cancer = tk.define('cancer', Bool(0.1))
    assert_equals(cancer.id, 'cancer')


@with_setup(setup, teardown)
def test_model_id_present_in_list():
    cancer = tk.define('cancer', Bool(0.1))
    assert_equals(tk.model_ids, ['cancer'])


@with_setup(setup, teardown)
def test_cannot_add_the_same_id():
    cancer = tk.define('cancer', Bool(0.1))
    assert_equals(tk.model_ids, ['cancer'])
    assert_raises(ValueError, tk.define, 'cancer', Bool(0.1))


@with_setup(setup, teardown)
def test_id_must_be_a_string():
    assert_raises(ValueError, tk.define, 2, Bool(0.1))


@with_setup(setup, teardown)
def test_lists_cardinalities():
    cancer = tk.define('cancer', Bool(0.1))
    cold = tk.define('cold', Bool(0.1))
    assert_equals(tk.number_models, 2)
    assert_equals(tk.cardinalities, {'cancer': 2, 'cold': 2})


@with_setup(setup, teardown)
def test_model_deletion():
    cancer = tk.define('cancer', Bool(0.1))
    cold = tk.define('cold', Bool(0.1))
    tk.delete('cold')
    assert_equals(tk.number_models, 1)
    tk.delete('cancer')
    assert_equals(tk.number_models, 0)
    assert_equals(tk.cardinalities, {})
    assert_equals(tk.models, {})


@with_setup(setup, teardown)
def test_cannot_delete_nonextant_model():
    cancer = tk.define('cancer', Bool(0.1))
    assert_equals(tk.model_ids, ['cancer'])
    assert_raises(ValueError, tk.delete, 'notcancer')

