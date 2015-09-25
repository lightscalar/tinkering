from tinkering.core.factor import *

class Model(object):

    def __init__(self):
        pass

    def depends_on(self, *models):
        for model in models:
            print 'Depends on %s ' % model.id