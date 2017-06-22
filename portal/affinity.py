from e5.algorithms import Algorithm
from e5.events import ContextFilter
from e5.portal import Panel
from e5.events.projections import Projection

import affinityPredictionAlgorithm as apa

# import affinityPredictionAlgorithm as apa

import numpy as np

class AffinityScoringAlgorithm(Algorithm):
    def __init__(self, id):
		self.id = id
        #selfs

    def getId(self):
        return self.id

    def predict(self, datapoints):
        prediction, algoDescription = apa.getAffinity(datapoints)
        predictionDict = self.dictify(prediction)

        # get the top five affinities to display in the panel
        affinities = {}
        values = list(predictionDict.values())
        keys = list(predictionDict.keys())
        for _ in range(5):
            maxIndex = values.index(max(values))
            affinities[keys[maxIndex]] = str(values[maxIndex])
            del values[maxIndex]
            del keys[maxIndex]

        return affinities

    def configure(self, configuration):
        if 'trainingData' in configuration:
            dataSet = configuration['trainingData'].getAll()
            self.targetLabels = {row[0]: row[1::] for index, row in dataSet.iterrows()}

    def train(self):
        return

    def getEvaluationStatus(self):
        return {'score': {'value': 0, 'name': ''}, 'stats': {}}

    def getLabel(self):
        return

    def getConfiguration(self):
        return self.configuration

    # probably unnecessary
    def __getScore(self, value):
        return

    def dictify(self, values):
        diction = {}
        branches = ['Beroepen bij de strijdkrachten','Leidinggevende functies',
        'Intellectuele, wetenschappelijke en artistieke beroepen',
        'Technici en vakspecialisten', 'Administratief personeel',
        'Dienstverlenend personeel en verkopers',
        'Geschoolde landbouwers, bosbouwers en vissers',
        'Ambachtslieden','Bedieningspersoneel van machines en installaties, assembleurs',
        'Elementaire beroepen']
        for i in range(0,len(values)):
            diction[branches[i]] = values[i]
        return diction

class AffinityPrediction(Panel):
    def __init__(self, event_stream, projection):
        self._event_stream = event_stream
        self._projection = projection

    def id(self):
        return "affinityPrediction"

    def update(self, requests, topics):
        return

    def applies(self, topics):
        return self.topicOfKind(topics, 'user')

    def getTemplateData(self, topics):
        if len(topics) != 0:
            if '_id' in topics[-1]:
                kind = topics[-1]['kind']
                topicid = topics[-1]['_id']
                context_filter = ContextFilter(topicid, kind)
                prediction = self._event_stream.get_projection(self._projection.id, context_filter)
                if len(prediction) > 0:
                    return prediction

        return {}

    def mode(self, topics):
        return "right"

    def getTemplate(self):
        return "lab1/affinity.html"

class AffinityAlgorithmProjection(Projection):
    def __init__(self, projection_id, attributes, algorithm):
        self._id = projection_id
        self._attributes = attributes
        self._algorithm = algorithm

    @property
    def id(self):
        return self._id

    def new_state(self, state, event):
        # get attributes values
        values = []
        # print "event attributes: "+str(len(event._attributes))
        # for elem in event._attributes:
        #     print elem, event._attributes[elem]
        for attribute in self._attributes:
            if attribute in event.attributes:
                values.append(int(event.attributes[attribute]))
            else:
                return state

        affinity = self._algorithm.predict(values)

        return {'prediction': affinity}

    def get_state_now(self, state):
        if state is None:
            return {}
        else:
            return state
