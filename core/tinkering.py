'''Core Tinkering class. Holds a Universe.'''
from pdb import set_trace as stop


class Tinkering(object):

    def __init__(self):
        self._models = {}
        self._model_ids = []
        self._network = {}

    @property
    def network(self):
        # Returns a list of all models attached to this Tinkering context.
        return self._network

    @property
    def models(self):
        # Returns a list of all models attached to this Tinkering context.
        return self._models

    @property
    def number_models(self):
        # Returns the number of models attached to this Tinkering context.
        return len(self._models)

    @property
    def model_ids(self):
        # Return a list of model IDs.
        return self._model_ids

    @property
    def cardinalities(self):
        # Return a list of the cardinalities of all models in the network.
        return {key: value.cardinality for (key, value) in \
                self.models.iteritems()}

    def define(self, model_id, model):
        # Define a new model in this Tinkering context.
        if type(model_id) != str:
            raise ValueError('Model name must be a string.')
        if model_id in self.model_ids:
            raise ValueError('Cannot add %s as a model because there is \
                    already a model with that name.' % model_id)
        model.id = model_id
        model.scope = [model.id]
        model.context = self
        self._models[model_id] = model
        self._model_ids.append(model_id)
        self._network[model.id] = model.dependencies
        model.update()
        return model

    def delete(self, model_or_id):
        # Remove a model from the network using a model instance or id.
        if type(model_or_id) == str:
            model_id = model_or_id
        else:
            model_id = model_or_id.id

        # Remove all instances of model from model and model_id dicts/lists.
        try:
            self._models.pop(model_id)
            self._model_ids.remove(model_id)
            del self._network[model_id]
            # Remove from all network dependencies.
            for key in self.network.keys():
                if model_id in self.models[key].scope:
                    self.models[key].scope.remove(model_id)
                    self.models[key].update()
                if model_id in self.network[key]:
                    self.network[key].remove(model_id)
        except:
            raise ValueError('Model "%s" does not exist. Cannot delete.' % \
                    model_id)






