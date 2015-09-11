from pyparsing import Word, alphas, nums, alphanums, OneOrMore, Literal, ZeroOrMore, OnlyOnce, Optional, ParseException,\
                        Suppress, delimitedList, oneOf


def convertFloats(data):
    return float(''.join(data).replace(',',''))

# Define floats, & other content.
floats = ZeroOrMore(Word(nums)) + Optional('.' + OneOrMore(Word(nums)))
floats.setName('float')
floats.setParseAction(convertFloats)
words = Word(alphanums).setName('word')
valid_content = floats ^ Word(alphanums)

# Parentheses.
lparen = Suppress('(')
rparen = Suppress(')')

# List.
float_list = delimitedList(valid_content)
arg_list =  lparen + float_list + rparen

# Data tags
data_tag = Literal('Data')
data_args = lparen + words('filename') + rparen
data = data_tag('type') + data_args

# Flip tags
flip_tag = Literal('Flip')
flip_args = lparen + floats('probability') + rparen
flip = flip_tag('type') + flip_args

# Variable names.
valid_variable_name = Word(alphas, alphanums + '_')
valid_distribution = flip('flip') ^ data('data')

# Assignment
assign_distribution = valid_variable_name('name') + Suppress('~') + valid_distribution('dist')
program = assign_distribution('assignment') ^ floats('float')

if __name__ == '__main__':
    grammar = program('program')
    tokens = grammar.parseString("cancer ~ Flip(0.2)")
    # grammar = commaSeparatedList('commas')
    # print grammar.parseString('2.0 43.2,3,4')
# print tokens == [1232.34]
