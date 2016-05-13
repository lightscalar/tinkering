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
                self.scope.append(model.id)

        # Need to update factor.
        self.update()

    def update(self):
        # Update things that need to be updated (factors, etc.)
        self.scope.sort()
        self._update_factor()

    @property
    def dependencies(self):
        return self._dependencies
