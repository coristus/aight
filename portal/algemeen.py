'''Algemene panelen t.b.v. van PiCompany's portaal i het HR Analytics Lab'''

from e5.portal import Panel, Topic
from e5.events import ContextFilter, AttributeFilter


class Teams(Panel):
    def __init__(self, d):
        self.data = d
    def id(self):
        return "teams"
    def update(self, request, topics):
        if request.args.get('id') is not None:
            obj = self.data.getObject(request.args.get('id'))
            if obj is not None:
                topic = Topic(obj['naam'], "users", obj)
                if topic not in topics:
                    topics.append(topic)

    def applies(self, topics):
        return self.topicOfKind(topics, 'home')

    def getTemplateData(self, topics):
        return {'teams': self.data.getAll()}

    def getTemplate(self):
        return "teams.html"

class AlgorithmsPanel(Panel):
    def id(self):
        return "algorithms"

    def update(self, request, topics):
        if request.args.get('id') is not None:
            topic = Topic(request.args.get('id'), "algorithm", {'id': request.args.get('id')})
            if topic not in topics:
                topics.append(topic)


    def applies(self, topics):
        return self.topicOfKind(topics, 'home')

    def getTemplateData(self, topics):
        return {}

    def mode(self, topics):
        return "right"

    def getTemplate(self):
        return "algorithms.html"

class AlgorithmDetailsPanel(Panel):
    def id(self):
        return "algorithmDetails"
    def update(self, request, topics):
        return

    def applies(self, topics):
        return self.topicOfKind(topics, 'algorithm')

    def getTemplateData(self, topics):
        return {}

    def getTemplate(self):
        return "algorithmdetails.html"

class AlgorithmTrainPanel(Panel):
    def id(self):
        return "algorithmtrain"
    def update(self, request, topics):
        return

    def applies(self, topics):
        return self.topicOfKind(topics, 'algorithm')

    def getTemplateData(self, topics):
        return {}

    def mode(self, topics):
        return "right";

    def getTemplate(self):
        return "algorithmtrain.html"

class AlgorithmScorePanel(Panel):
    def id(self):
        return "algorithmScore"
    def update(self, request, topics):
        return

    def applies(self, topics):
        return self.topicOfKind(topics, 'algorithm')

    def getTemplateData(self, topics):
        return {}

    def mode(self, topics):
        return "right"

    def getTemplate(self):
        return "algorithm_score.html"

class AlgorithmStatsPanel(Panel):
    def id(self):
        return "algorithmStats"
    def update(self, request, topics):
        return

    def applies(self, topics):
        return self.topicOfKind(topics, 'algorithm')

    def getTemplateData(self, topics):
        return {}

    def getTemplate(self):
        return "algorithm_stats.html"

class Medewerkers(Panel):
    def __init__(self, d):
        self.data = d
    def id(self):
        return "medewerkers"
    def update(self, request, topics):
        if request.args.get('id') is not None:
            obj = self.data.getObject(request.args.get('id'))
            if obj is not None:
                topic = Topic(obj['naam'], "user", obj)
                if topic not in topics:
                    topics.append(topic)

    def applies(self, topics):
        return self.topicOfKind(topics, 'home')

    def getTemplateData(self, topics):
        return {'medewerkers': self.data.getAll()}

    def getTemplate(self):
        return "medewerkers.html"

class TeamMedewerkers(Panel):
    def __init__(self, d):
        self.data = d

    def id(self):
        return "teamMedewerkers"

    def update(self, request, topics):
        if request.args.get('id') is not None:
            mdw = self.data.getObject(request.args.get('id'))
            if mdw is not None:
                topic = Topic(mdw['naam'], "user", mdw)
                if topic not in topics:
                    topics.append(topic)

    def mode(self, topics):
        return "right"

    def applies(self, topics):
        return self.topicOfKind(topics, 'users')

    def getTemplateData(self, topics):
        return {'medewerkers': self.data.getFiltered("team", topics[len(topics)-1]['topic'])}

    def getTemplate(self):
        return "teammedewerkers.html"

class TeamMedewerkersFilter(Panel):
    def __init__(self, event_stream, projection):
        self._event_stream = event_stream
        self._projection = projection

    def id(self):
        return "teammedewerkers-filter"

    def update(self, request, topics):
        if request.args.get('id') is not None:
            mdw = self._event_stream.get_context_by_id(request.args.get('id'))
            if mdw is not None:
                topic = Topic(mdw.attributes['naam'], "user", mdw.dict)
                if topic not in topics:
                    topics.append(topic)

    def mode(self, topics):
        return "main"

    def applies(self, topics):
        return self.topicOfKind(topics, 'users')

    def getTemplateData(self, topics):
        topic = topics[len(topics)-1]['topic']
        attrbitute_filter = AttributeFilter("team", topic)
        medewerkers = self._event_stream.get_contexts(attribute_filters=[attrbitute_filter])
        joined_mdw = []
        for medewerker in medewerkers:
            context_filter = ContextFilter(medewerker.context_id, 'user')
            personality = self._event_stream.get_projection(self._projection.id, context_filter)
            if len(personality) > 0:
                medewerker.attributes.update(personality)
            joined_mdw.append(medewerker)

        return {'medewerkers': joined_mdw}

    def getTemplate(self):
        return "teammedewerkers-filter.html"


class BigFiveBars(Panel):
    def __init__(self, event_stream, projection):
        self._event_stream = event_stream
        self._projection = projection

    def id(self):
        return "bigFiveBars"

    def update(self, request, topics):
        return

    def applies(self, topics):
        return self.topicOfKind(topics, 'user')

    def getTemplateData(self, topics):
        if 'id' in topics[len(topics)-1]:
            kind = topics[len(topics)-1]['kind']
            topicid = topics[len(topics)-1]['id']
            context_filter = ContextFilter(topicid, kind)
            personality = self._event_stream.get_projection(self._projection.id, context_filter)
            if len(personality) > 0:
                return {"persoonlijkheid": personality}
        return {}

    def getTemplate(self):
        return "bigfive_bars.html"

class BigFiveTable(Panel):
    def __init__(self, event_stream, projection):
        self._event_stream = event_stream
        self._projection = projection

    def id(self):
        return "bigFiveTable"

    def mode(self, topics):
        return "right"

    def update(self, request, topics):
        return

    def applies(self, topics):
        return self.topicOfKind(topics, 'user')

    def getTemplateData(self, topics):
        if 'id' in topics[len(topics)-1]:
            kind = topics[len(topics)-1]['kind']
            topicid = topics[len(topics)-1]['id']
            context_filter = ContextFilter(topicid, kind)
            personality = self._event_stream.get_projection(self._projection.id, context_filter)
            if len(personality) > 0:
                return {"persoonlijkheid": personality}
        return {}

    def getTemplate(self):
        return "bigfive_table.html"
