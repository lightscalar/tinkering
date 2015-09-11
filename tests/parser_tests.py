# from tinkering_beta.basics import *
# from nose.tools import assert_equals, assert_almost_equals, assert_raises
# from nose import with_setup
# from numpy.testing import assert_array_almost_equal_nulp, assert_array_equal


# def setup():
#     pass


# def teardown():
#     pass


# # BEGIN TESTS ------------------------------------------------------
# @with_setup(setup, teardown)
# def test_parse_floats():
#     grammar = floats('float')
#     tokens = grammar.parseString('1,232.67')
#     assert_equals(tokens.float, 1232.67)


# def test_parse_floats_2():
#     grammar = floats('float')
#     tokens = grammar.parseString('.67')
#     assert_equals(tokens.float, 0.67)


# def test_parse_floats_3():
#     grammar = floats('float')
#     tokens = grammar.parseString('.1415')
#     assert_equals(tokens.float, 0.1415)


# def test_valid_variable_name():
#     grammar = valid_variable_name('var')
#     tokens = grammar.parseString('lung_cancer')
#     assert_equals(tokens.var, 'lung_cancer')


# def test_bad_names():
#     grammar = valid_variable_name('var')
#     assert_raises(ParseException, grammar.parseString, '42_lung_cancer')
#     assert_raises(ParseException, grammar.parseString, '_lung_cancer')
#     assert_raises(ParseException, grammar.parseString, '!lung_cancer')


# def test_distribution_names():
#     grammar = valid_distribution_names('var')
#     assert_equals(grammar.parseString('Normal').var, 'Normal')
#     assert_equals(grammar.parseString('Flip').var, 'Flip')
#     assert_equals(grammar.parseString('Poisson_22').var, 'Poisson_22')


# def test_bad_distribution_names():
#     grammar = valid_distribution_names('var')
#     assert_raises(ParseException, grammar.parseString, 'normal')
#     assert_raises(ParseException, grammar.parseString, '22-Normal')
#     assert_raises(ParseException, grammar.parseString, '_Normal')


# def test_create_distribution():
#     grammar = assign_distribution('assign')
#     parse = grammar.parseString('cancer ~ Flip(0.2)')
#     assert_equals





