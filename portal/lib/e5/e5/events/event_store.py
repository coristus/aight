'''Eventstore module'''
import datetime
from e5.events import Event
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId

class EventStore(object):
    '''Eventstore interface'''
    def store(self, event):
        '''Store an event in the evenstore'''
        pass

    def find(self):
        '''Get all events from database'''
        pass

    def delete(self, event_id):
        '''Remove events from database'''
        pass

    def find_by_id(self, event_id):
        '''Find event by id from database'''
        pass

    def update(self, event_id, fields):
        pass

    def find_one(self, query):
        '''Get an event based on filtering'''
        pass

    def query(self, event_types, context_filters, from_time, to_time, source):
        ''' Query store '''
        pass

    def clear(self):
        ''' clear all events '''
        pass

class MongoEventStore(EventStore):
    '''MongoDB event store implementation'''

    def __init__(self, collection):
        self._collection = collection

    def store(self, event):
        if not isinstance(event, Event):
            raise TypeError('This is not an event object')

        return self._collection.insert_one(event.dict).inserted_id

    def find(self):
        return self._query({})

    def delete(self, event_id):
        return self._collection.delete_one({'_id': ObjectId(event_id)})

    def find_by_id(self, event_id):
        return self.find_one({'_id': ObjectId(event_id)})

    def find_one(self, query):
        event_dict = self._collection.find_one(query)
        return Event.from_dict(event_dict)

    def update(self, event_id, fields):
        return self._collection.update_one({"_id": event_id}, {"$set": fields}, True)

    def query(self, event_types=[], context_filters=[], from_time=None, to_time=None, source=None):
        query = {}

        if from_time != None and not isinstance(from_time, datetime.datetime):
            raise TypeError('from_time is not a datetime instance')

        if to_time != None and not isinstance(to_time, datetime.datetime):
            raise TypeError('to_time is not a datetime instance')

        requirements = []
        if len(event_types) > 0:
            requirements.append({'$or': [{'header.type': event_type} for event_type in event_types]})

        if len(context_filters) > 0:
            contexts_query = []
            for context_filter in context_filters:
                sub_query = [
                    {'contexts.contextType': context_filter.context_type},
                    {'contexts.id': context_filter.context_id}
                ]

                if context_filter.context_role is not None:
                    sub_query.append({'contexts.contextRole': context_filter.context_role})

                contexts_query.append({'$and': sub_query})

            requirements.append({'$and': contexts_query}) #TODO: should this be AND or OR?

        if from_time != None:
            requirements.append({'header.date': {'$gte': from_time}})

        if to_time != None:
            requirements.append({'header.date': {'$lte': to_time}})

        if source != None:
            requirements.append({'header.source': source})

        if len(requirements) > 0:
            query['$and'] = requirements

        print query

        return self._query(query)


    def _query(self, query):
        return self._return_events(self._collection.find(query).sort('header.date', ASCENDING))

    def _return_events(self, event_dicts):
        events = []
        for event_dict in event_dicts:
            events.append(Event.from_dict(event_dict))

        return events

    def clear(self):
        self._collection.delete_many({})
