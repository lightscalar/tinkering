from tinkering.core.factor import *
from pdb import set_trace as stop

class Model(object):

    def __init__(self):
        self._dependencies = []

    def depends_on(self, *models):
        # Assigns dependencies to this model.
        for model in models:
            if model.id not in self._dependencies:
                self._dependencies.append(model.id)

    @property
    def dependencies(self):
        return self._dependencies
