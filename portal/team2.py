from e5.algorithms import Algorithm
from e5.events import ContextFilter
from e5.portal import Panel
from e5.events.projections import Projection

import numpy as np

class FunctionPredictionAlgorithm(Algorithm):
    def __init__(self, id):
        self.id = id
        self.configuration = {}
        self.stats = {}
        self.trainingDataSize = 0
        self.targetLabels = {}

    def getId(self):
        return self.id

    def predict(self, datapoints):
        return

    def configure(self, configuration):
        return

    def train(self):
        return

    def getEvaluationStatus(self):
        return

    def getLabel(self):
        return

    def getConfiguration(self):
        return self.configuration

class UitsprakenPrediction(Panel):
    def __init__(self, event_stream, projection):
        self._event_stream = event_stream
        self._projection = projection

    def id(self):
        return "uitsprakenPrediction"

    def update(self, request, topics):
        return

    def applies(self, topics):
        return self.topicOfKind(topics, 'user')

    def getTemplateData(self, topics):
        if '_id' in topics[len(topics)-1]:
            kind = topics[len(topics)-1]['kind']
            topicid = topics[len(topics)-1]['_id']
            context_filter = ContextFilter(topicid, kind)
            prediction = self._event_stream.get_projection(self._projection.id, context_filter)
            if len(prediction) > 0:
                return prediction

        return {}

    def mode(self, topics):
        return "right"

    def getTemplate(self):
        return "uitspraken.html"

class UitsprakenAlgorithmProjection(Projection):
    def __init__(self, projection_id, attributes, algorithm):
        self._id = projection_id
        self._attributes = attributes
        self._algorithm = algorithm

    @property
    def id(self):
        return self._id

    def new_state(self, state, event):
        # get the attributes values
        values = []
        for attribute in self._attributes:
            if attribute in event.attributes:
                values.append(int(event.attributes[attribute]))
            else:
                return state

        prediction = self._algorithm.predict(values)
        # TODO generate 'uitspraken' based on the prediction
        return {'prediction': prediction}

    def get_state_now(self, state):
        if state is None:
            return {}
        else:
            return state