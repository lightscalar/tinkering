'''Utility functions for processing numerical data.'''


def is_numeric(value):
    '''Determine if a value is numeric.'''
    try:
        float(value)
        return True
    except:
        return False


def estimate_data_type(data_samples):
    '''Characterize the data's type. Will return either :categorical or
       :numeric.'''
    for sample in data_samples:
        if not is_numeric(sample):
            return 'categorical'
    return 'numeric'
