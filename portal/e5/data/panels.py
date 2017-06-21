from e5.portal import Topic, BasePanel
from e5.events import ContextFilter

class DataMasterPanel(BasePanel):
    def __init__(self, panelid, keycolumn, labelcolumn, data, icon="user", panelType="main", label="Alle objecten", template="data/master.html", projections=None, event_stream=None):
        self._data = data
        self._id = panelid
        self._label = label
        self._keycolumn = keycolumn
        self._labelcolumn = labelcolumn
        self._icon = icon
        self.panelType = panelType
        self._template = template
        self._projections = projections
        self._event_stream = event_stream

    def id(self):
        return self._id

    def update(self, request, topics):
        if request.args.get(self._keycolumn) is not None:
            obj = self._data.getObject(request.args.get(self._keycolumn))
            if obj is not None:
                topic = Topic(obj[self._labelcolumn], self._icon, obj)
                topic['_id'] = obj[self._keycolumn]
                topics.append(topic)

    def applies(self, topics):
        return self.topicOfKind(topics, 'home')

    def getTemplateData(self, topics):

        objects = self._data.getAll()

        if self._projections is not None:
            for obj in objects:
                if 'projections' not in obj:
                    obj['projections'] = {}
                for projection in self._projections:
                    context_filter = ContextFilter(obj[self._keycolumn], self._icon)
                    value = self._event_stream.get_projection(projection, context_filter)
                    obj['projections'][projection] = value

        return {
            'id': self._id,
            'label': self._label,
            'keycol': self._keycolumn,
            'labelcol': self._labelcolumn,
            'objects': objects,
            'icon': self._icon
        }

    def getTemplate(self):
        return self._template


## class DataDetailPanel(BasePanel):
