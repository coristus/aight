'''Submit handlers module'''
import datetime
from dateutil import parser
from e5.events import Event, Context

from e5.portal import SubmitHandler

class EventStoreHandler(SubmitHandler):
    ''' store submitted events'''

    def __init__(self, event_stream, event_type, topic_role, submit_date_field=None, user_role=None):
        self._event_stream = event_stream
        self._event_type = event_type
        self._submit_date_field = submit_date_field
        self._topic_role = topic_role
        self._user_role = user_role

    def handle(self, topic, form_id, form_data, user):
        context = Context(topic['kind'], {})
        context.context_id = topic['_id'] # technical depth
        contexts = {self._topic_role: [context]}

        if self._user_role is not None:
            user_context = Context('user', {})
            user_context.context_id = user.get_id()
            contexts[self._user_role] = [user_context]

        date = datetime.datetime.now()

        if self._submit_date_field is not None:
            date = parser.parse(form_data[self._submit_date_field])

        event = Event(
            self._event_type,
            date,
            form_id,
            contexts,
            form_data
        )


        return self._event_stream.push(event)

class UserStoreHandler(SubmitHandler):
    ''' store submitted events'''

    def __init__(self, user_store, context_store, context_type):
        self._user_store = user_store
        self._context_store = context_store
        self._context_type = context_type

    def handle(self, topic, form_id, form_data, user):
        if 'fullname' not in form_data:
            raise Exception('fullname not in form')

        if 'username' not in form_data:
            raise Exception('username not in form')

        if 'password' not in form_data:
            raise Exception('password not in form')

        full_name = form_data['fullname']
        username = form_data['username']
        password = form_data['password']

        user_id = self._user_store.store(full_name, username, password)

        print 'Created user with id', user_id

        del form_data['password']
        form_data['naam'] = full_name
        context = Context(self._context_type, form_data)
        context.context_id = user_id

        context_id = self._context_store.store(context)

        print 'Created context with id', context_id

        return user_id, context_id

class ContextStoreHandler(SubmitHandler):
    ''' store submitted events'''

    def __init__(self, context_store, context_type, fields=[]):
        self._context_store = context_store
        self._context_type = context_type
        self._fields = fields

    def handle(self, topic, form_id, form_data, user):
        data = form_data
        if len(self._fields) > 0:
            data = {key: form_data[key] for key in self._fields}
        context = Context(self._context_type, data)
        return self._context_store.store(context)
