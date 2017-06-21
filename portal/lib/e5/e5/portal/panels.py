## Portal API

import sys
import json

from e5.events.event_stream import EventStream
from e5.portal import Panel, BasePanel, Topic
from e5.events import ContextFilter

from flask import make_response

class ContextListPanel(Panel):
    def __init__(self, event_stream, context_type, id, key, topic, topic_kind, mode, endpoint):
        self._event_stream = event_stream
        self._context_type = context_type
        self._key = key
        self._id = id
        self._topic = topic
        self._topic_kind = topic_kind
        self._mode = mode
        self._endpoint = endpoint

    def id(self):
        return self._id

    def update(self, request, topics):
        if request.args.get('id') is not None:
            obj = self._event_stream.get_context_by_id(request.args.get('id'))
            if obj is not None:
                topic = Topic(obj.attributes[self._key], self._topic, obj.dict)#technical depth
                if topic not in topics:
                    topics.append(topic)

    def mode(self, topics):
        return self._mode

    def applies(self, topics):
        return self.topicOfKind(topics, self._topic_kind)

    def getTemplateData(self, topics):
        contexts = self._event_stream.get_contexts(context_types=[self._context_type])

        transformed_contexts = []
        found_values = []
        for context in contexts:
            if self._key in context.attributes and context.attributes[self._key] not in found_values:
                transformed_contexts.append(
                    {'id': context.context_id, 'value': context.attributes[self._key]}
                )
                found_values.append(context.attributes[self._key])

        return {'contexts': transformed_contexts, 'endpoint': self._endpoint}

    def getTemplate(self):
        return "panels/e5contextpanel.html"


class MockupPanel(BasePanel):
    def update(self, request, topics):
        return
    def getTemplateData(self, topics):
        return {}
    def getTemplate(self):
        return self.template

class AllFormsPanel(BasePanel):
    def __init__(self, panelID, topicKind, panelType, forms, kind_map={}):
        self.panelID = panelID
        self.topicKind = topicKind
        self.panelType = panelType
        self.forms = forms
        self._kind_map = kind_map

    def getTemplateData(self, topics):
        return {
            'forms': [
                {"id": form.id, "label": form.label} 
                for form in self.forms 
                if len(self._kind_map) == 0 or (self.topicKind in self._kind_map and form.id in self._kind_map[self.topicKind])
            ]
        }

    def getTemplate(self):
        return "panels/e5allformspanel.html"

class EventsPanel(BasePanel):
    def __init__(self, panelID, topicKind, panelType, eventStream, details="panels/e5timeline-details.html"):
        self.panelID = panelID
        self.topicKind = topicKind
        self.panelType = panelType
        self.eventStream = eventStream
        self._details = details

    def getTemplateData(self, topics):
        kind = topics[len(topics)-1]['kind']
        id = topics[len(topics)-1]['_id']
        print kind, id
        context_filter = ContextFilter(id, kind)
        # query all events with (kind, id) as context (in any role....)
        # events = self.eventStream.get_events();
        events = reversed(self.eventStream.get_events(context_filters = [context_filter]))

        return {'details': self._details, 'events': events}

    def getTemplate(self):
        return "panels/e5timeline.html"

class ProjectionsPanel(Panel):

    def __init__(self, id, event_stream, projections, template="panels/e5projections.html", topicType="user"):
        self.event_stream = event_stream
        self.projections = projections
        self._template = template
        self._id = id
        self._topicType = topicType

    def id(self):
        return self._id

    def update(self, request, topics):
        pass

    def applies(self, topics):
        return self.topicOfKind(topics, self._topicType)

    def getTemplateData(self, topics):
        kind = topics[len(topics)-1]['kind']
        topicid = topics[len(topics)-1]['_id']

        data = []
        for projection in self.projections:
            context_filter = ContextFilter(topicid, kind)
            data.append(
                {
                    'id': projection,
                    'value': self.event_stream.get_projection(projection, context_filter)}
                )

        sys.stderr.write(str({'projections': data})+'\n')
        return {'projections': data}

    def getTemplate(self):
        return self._template

class SankeyPanel(Panel):
    def __init__(self, event_stream, projection):
        self.event_stream = event_stream
        self.projection = projection

    def id(self):
        return "sankey"

    def update(self, request, topics):
        pass

    def applies(self, topics):
        return self.topicOfKind(topics, 'user') or self.topicOfKind(topics, 'home')

    def getTemplateData(self, topics):
        kind = topics[len(topics)-1]['kind']
        topicid = None

        if 'id' in topics[len(topics)-1]:
            topicid = topics[len(topics)-1]['_id']

        if kind == 'user':
            context_filter = ContextFilter(topicid, kind)
            data = {
                'sankey': self.event_stream.get_projection(self.projection, context_filter)
                }
        else:
            data = {'sankey': self.event_stream.get_projection(self.projection)}

        return data

    def getTemplate(self):
        return "panels/e5sankey.html"

    def renderResource(self, uri, topics=[]):
        kind = topics[len(topics)-1]['kind']
        topicid = None

        if '_id' in topics[len(topics)-1]:
            topicid = topics[len(topics)-1]['_id']

        if kind == 'user':
            context_filter = ContextFilter(topicid, kind)
            json_data = json.dumps(self.event_stream.get_projection(self.projection, context_filter))
        else:
            json_data = json.dumps(self.event_stream.get_projection(self.projection))

        response=make_response(json_data)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
