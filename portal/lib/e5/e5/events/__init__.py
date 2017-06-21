''' Models module'''
from dateutil import parser

class AttributeFilter(object):
    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value


class ContextFilter(object):
    def __init__(self, context_id, context_type):
        self._context_id = context_id
        self._context_type = context_type
        self._context_role = None

    @property
    def context_id(self):
        return self._context_id

    @property
    def context_type(self):
        return self._context_type

    @property
    def context_role(self):
        return self._context_role

    @context_role.setter
    def context_role(self, value):
        self._context_role = value

class EventType(object):
    '''EventType'''

    def __init__(self, id, label, attributes):
        self._id = id
        self._label = label
        self._attributes = attributes

    @property
    def id(self):
        '''get id'''
        return self._id

    @property
    def label(self):
        '''get label'''
        return self._label

    @property
    def attributes(self):
        '''get the attributes'''
        return self._attributes

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class ContextType(object):
    '''context type'''

    def __init__(self, id, label, contexts):
        self._id = id
        self._label = label
        self._contexts = contexts

    @property
    def id(self):
        '''get id'''
        return self._id

    @property
    def label(self):
        '''get context type label'''
        return self._label

    @property
    def contexts(self):
        '''get contexts'''
        return self._contexts

    def search_contexts(self, context_id):
        '''get context by id'''
        for context in self._contexts:
            if context.context_id == context_id:
                return context

        return None

class ContextRole(object):
    '''ContextRole'''

    def __init__(self, label):
        self._label = label

    @property
    def label(self):
        '''get label'''
        return self._label

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class Context(object):
    '''Context'''

    def __init__(self, context_type, attributes):
        self._context_type = context_type
        self._attributes = attributes
        self._id = ''

    @property
    def context_id(self):
        '''id'''
        return self._id

    @context_id.setter
    def context_id(self, value):
        self._id = value

    @property
    def context_type(self):
        '''Type of context'''
        return self._context_type

    @context_type.setter
    def context_type(self, value):
        self._context_type = value

    @property
    def attributes(self):
        '''Context attributes'''
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value


    @property
    def dict(self):
        '''Return context as dictionary'''
        context_dict = {
            'contextType': self._context_type,
            'attributes': self._attributes
        }

        if self._id != '':
            context_dict['_id'] = self._id

        return context_dict

    @staticmethod
    def from_dict(context_dict):
        '''Create context from dictionary'''

        attributes = {}
        if 'attributes' in context_dict:
            attributes = context_dict['attributes']

        context = Context(
            context_dict['contextType'],
            attributes
        )

        if '_id' in context_dict:
            context.context_id = str(context_dict['_id'])

        return context

    def __hash__(self):
        return hash((self.context_id, self.context_type))

    def __eq__(self, other):
        return (self.context_id, self.context_type) == (other.context_id, other.context_type)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

class Event(object):
    '''Event'''

    def __init__(self, event_type, date, source, contexts, attributes):
        self._event_type = event_type
        self._date = date
        self._source = source
        self._contexts = contexts
        self._attributes = attributes
        self._id = ''

    @property
    def id(self):
        '''Id of event'''
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def event_type(self):
        '''Type of event'''
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        self._event_type = value

    @property
    def date(self):
        '''Moment the event was created'''
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def source(self):
        '''The source where this Event
           originates from
        '''
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def contexts(self):
        '''Get contexts'''
        return self._contexts

    @contexts.setter
    def contexts(self, value):
        self._contexts = value

    @property
    def attributes(self):
        '''Get event attributes'''
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value

    @property
    def dict(self):
        '''Return event as dictionary'''
        event_dict = {
            'header': {
                'type': self._event_type,
                'date': self._date.isoformat(),
                'source': self._source
            },
            'contexts': [
                {
                    'contextRole': key,
                    'id': context.context_id,
                    'contextType': context.context_type
                }
                for key, contexts in self._contexts.iteritems() for context in contexts
            ],
            'attributes': self._attributes
        }

        if self._id != '':
            event_dict['_id'] = str(self._id)

        return event_dict

    @staticmethod
    def from_dict(event_dict):
        '''Create event from dictionary'''
        header = event_dict['header']

        contexts = {}
        for context_dict in event_dict['contexts']:
            context_role = context_dict['contextRole']
            del context_dict['contextRole']

            context = Context.from_dict(context_dict)
            if context_role in contexts:
                contexts[context_role].append(context)
            else:
                contexts[context_role] = [context]

        attributes = {}
        if 'attributes' in event_dict:
            attributes = event_dict['attributes']

        event = Event(
            header['type'],
            parser.parse(header['date']),
            header['source'],
            contexts,
            attributes
            )

        if '_id' in event_dict:
            event.id = event_dict['_id']

        return event
