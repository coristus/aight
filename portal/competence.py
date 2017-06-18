from e5.algorithms import Algorithm
from e5.events import ContextFilter
from e5.portal import Panel
from e5.events.projections import Projection

import numpy as np

class CompetenceDevelopmentScoringAlgorithm(Algorithm):
    def __init__(self, id):
        self.id = id
        self.configuration = {'cutOff': 3.5}
        self.stats = {}
        self.trainingDataSize = 0
        self.targetLabels = {}

    def getId(self):
        return self.id

    def predict(self, datapoints):
        competences = {}
        for competence, row in self.targetLabels.iteritems():
            important_competences = sum(row)
            value = self.__getScore(np.dot(datapoints, row) / float(important_competences))
            if value > self.configuration['cutOff']:
                competences[competence] = value

        return competences

    def configure(self, configuration):
        if 'cutOff' in configuration:
            self.configuration['cutOff'] = configuration['cutOff']

        if 'trainingData' in configuration:
            dataset = configuration['trainingData'].getAll()
            self.targetLabels = {row[0]: row[1::] for index, row in dataset.iterrows()}


    def train(self):
        return

    def getEvaluationStatus(self):
        return {'score': {'value': 0, 'name': ''}, 'stats': {}}

    def getLabel(self):
        return

    def getConfiguration(self):
        return self.configuration

    def __getScore(self, value):
        if value > 35 and value <= 45:
            return 2
        elif value > 45 and value <= 55:
            return 3
        elif value > 55 and value <= 65:
            return 4
        elif value > 65:
            return 5
        return 1

class CompetencePrediction(Panel):
    def __init__(self, event_stream, projection):
        self._event_stream = event_stream
        self._projection = projection

    def id(self):
        return "competencePrediction"

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
        return "lab1/competence.html"

class CompetenceAlgorithmProjection(Projection):
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

        competence = self._algorithm.predict(values)

        return {'prediction': competence}

    def get_state_now(self, state):
        if state is None:
            return {}
        else:
            return state