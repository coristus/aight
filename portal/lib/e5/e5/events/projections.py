''' Projections module'''
import abc
from datetime import datetime, timedelta

class Projection(object):
    '''Projection interface'''
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def id(self):
        raise NotImplementedError('Must provide implementation in subclass.')

    @abc.abstractmethod
    def new_state(self, old_state, event):
        ''' update projection state based on newly occurred event '''
        raise NotImplementedError('Must provide implementation in subclass.')


    @abc.abstractmethod
    def get_state_now(self, state):
        ''' before showing/using the projection, compensate for current wallclock time '''
        raise NotImplementedError('Must provide implementation in subclass.')

class LatestAndGreatestProjection(Projection):
    """ Infer the latest value of an attribute as observed in the event stream. """

    def __init__(self, projection_id, attributes):
        self._id = projection_id
        self._attributes = attributes

    @property
    def id(self):
        return self._id

    def new_state(self, state, event):
        if state is None:
            state = {}

        for attr in self._attributes:
            if attr in event.attributes:
                state[attr] = event.attributes[attr]

        return state

    def get_state_now(self, state):
        if state is None:
            return {'object': {}}
        else:
            return {'object': state }

class TrendProjection(Projection):
    """ Infer whether a trend is obvious in the values of a gove attribute."""

    def __init__(self, projection_id, attribute):
        self._id = projection_id
        self.attribute = attribute

    @property
    def id(self):
        return self._id

    def new_state(self, state, event):
        if state is None:
            state = {'sum': 0, 'count': 0}
        if self.attribute in event.attributes:
            state['sum'] += event.attributes[self.attribute]
            state['count'] += 1
            state['last_value'] = event.attributes[self.attribute]
        return state

    def get_state_now(self, state):
        if state is None:
            return {"trend": None}
        else:
            avg = state.sum/state.count
            if avg > 1.2 * state.last_value:
                return {"trend": 'Up'}
            if avg < 0.8 * state.last_value:
                return {"trend": 'Down'}
            else:
                return {"trend": 'Equal'}



class TermijnProjection(Projection):
    """ Infer the time spent "active" based on a number of start events and a number of stop events."""

    def __init__(self, projection_id, start_events, stop_events):
        self._id = projection_id
        self._start_events = start_events
        self._stop_events = stop_events

    @property
    def id(self):
        return self._id

    def new_state(self, state, event):
        if state is None:
            state = {"duration": timedelta(), "lastStarted": None}

        if state['lastStarted'] is None and event.event_type in self._start_events:
            state['lastStarted'] = event.date

        if state['lastStarted'] is not None and event.event_type in self._stop_events:
            state['duration'] = state['duration'] + (event.date - state['lastStarted'])
            state['lastStarted'] = None

        # print "After "+event.event_type+":"+str(state)+"\n"
        return state

    def get_state_now(self, state):
        if state is None:
            return {"duration": 0}
        if state['lastStarted']is None:
            return {"duration": state['duration']}
        else:
            return {"duration": state['duration'] + (datetime.now() - state['lastStarted'])}

class SankeyProjection(Projection):
    def __init__(self, projection_id, context_role, mapping):
        self._mapping = mapping
        self._id = projection_id
        self._context_role = context_role

    @property
    def id(self):
        return self._id

    def new_state(self, projection_state, event):
        if projection_state == None:
            projection_state = {
                # last_context_state: (context -> latestState)
                'last_context_state': {},

                # all_states: [state, ..., ...]
                'all_states': [],

                # transitions: ((old,new) -> count)
                'transition_count' : {}
            }

        # HELP
        if self._context_role not in event.contexts:
            return projection_state

        for context in event.contexts[self._context_role]:

            last_state = None
            if context in projection_state['last_context_state']:
                last_state = projection_state['last_context_state'][context]

            # Compute new state for this context
            new_state = self._mapping[event.event_type](last_state, event) if event.event_type in self._mapping else last_state

            if (new_state is not None and new_state not in projection_state['all_states']):
                projection_state['all_states'].append(new_state)

            if (new_state != last_state and last_state != None):
                transition = (last_state, new_state)
                print "[Sankey] Transition found: " + str(transition) + " for " + str(context.context_id)
                # count transition_counts
                if transition in projection_state['transition_count']:
                    projection_state['transition_count'][transition] = projection_state['transition_count'][transition] + 1
                    print "[Sankey] Incrementing: " + str(transition)
                else:
                    projection_state['transition_count'][transition] = 1

            projection_state['last_context_state'][context] = new_state

        return projection_state

    def get_state_now(self, state):
        """ Return the sankey projection state in the format that the Javscript Sankey lib understands... . """
        if state is None:
            return {}

        labels = state['all_states']

        return {
            "nodes": [{"name": n} for n in state['all_states']],
            "T": len(state['transition_count']),
            "links": [{"source": labels.index(t[0]), "target" : labels.index(t[1]), "value": value} for t, value in state['transition_count'].iteritems()]
        }
