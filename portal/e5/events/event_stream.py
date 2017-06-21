''' stream '''
from e5.events.event_store import EventStore
from e5.events.context_store import ContextStore
from e5.events import Event, EventType, ContextType, ContextFilter
from e5.events.projections import Projection


class EventStreamCache:
    def __init__(self):
        self.cache = {}
        self._projections = []

    def register_projection(self, projection):
        """ update the current value for this projection in cache???"""
        """ CURRENT CODE
            # initialize current_states...
            events = self.get_events()

            state = None
            for event in events:
                state = projection.new_state(state, event)
            self._current_states[projection.id] = state
        """
        """ invoke super """

    def push(self, event):
        print "do something smart with cache"

    def get_projection(projection_id, context, contextRole=None, at_time=None):
        print "use cache under certain conditions, or else delegate (and update cache"

    """
    # TODO Should be moved to cache
    def update_projections(self, event):
        for p_id in self._projections:
            state = None
            if p_id in self._current_states:
                state = self._current_states[p_id]

            projection = self._projections[p_id]

            self._current_states[p_id] = projection.new_state(state, event)
    """

event_stream_cache = EventStreamCache()



class EventStream(object):
    ''' stream '''

    def __init__(self):
        self._event_store = None
        self._context_store = None
        self._event_types = []
        self._projections = {}
        self._context_types = []
        self._current_states = {}

    def register_event_store(self, store):
        if not isinstance(store, EventStore):
            raise TypeError('This is not an EventStore instance')

        self._event_store = store

    def register_context_store(self, store):
        if not isinstance(store, ContextStore):
            raise TypeError('This is not a ContextStore instance')

        self._context_store = store

    def register_event_type(self, event_type):
        if not isinstance(event_type, EventType):
            raise TypeError('This is not an EventType instance')

        self._event_types.append(event_type)

    def register_context_type(self, context_type):
        if not isinstance(context_type, ContextType):
            raise TypeError('This is not an EventType instance')

        self._context_types.append(context_type)

    def register_projection(self, projection):
        if not isinstance(projection, Projection):
            raise TypeError('This is not an Projection instance')

        self._projections[projection.id] = projection

    def push(self, event):
        ''' pushes an event to the stream '''
        if not isinstance(event, Event):
            raise TypeError('This is not an Event instance')

        return self._event_store.store(event)

    def delete_event(self, event_id):
        return self._event_store.delete(event_id)

    def get_event_id(self, event_id):
        return self._event_store.find_by_id(event_id)

    def get_events(self, event_types=[], context_filters=[], from_time=None, to_time=None, source=None):
        return self._event_store.query(event_types, context_filters, from_time, to_time, source)

    def get_projection(self, projection_id, context_filter=None, at_time=None):
        filters = []
        if context_filter is not None:
            filters.append(context_filter)
        events = self.get_events(context_filters=filters, to_time=at_time)

        state = None
        projection = self._projections[projection_id]

        for event in events:
            state = projection.new_state(state, event)

        return projection.get_state_now(state)

    def get_context_by_id(self, context_id):
        return self._context_store.find_by_id(context_id)

    def get_contexts(self, context_types=[], attribute_filters=[]):
        return self._context_store.query(context_types, attribute_filters)

    def get_contexts_with_projections(self, context_types=[], attribute_filters=[], projections=[]):

        contexts = self._context_store.query(context_types, attribute_filters)
        for context in contexts:
            if 'projections' not in context:
                context['projections'] = {}

            for projection in projections:
                context_filter = ContextFilter(context.context_id, context.context_type)
                value = self.get_projection(projection, context_filter)
                context['projections'][projection] = value
                
        return contexts
