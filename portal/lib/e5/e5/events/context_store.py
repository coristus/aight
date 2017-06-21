
'''Contextstore module'''
from e5.events import Context
from bson.objectid import ObjectId

class ContextStore(object):
    '''Contextstore interface'''
    def store(self, context):
        '''Store an event in the evenstore'''
        pass

    def find_by_id(self, context_id):
        '''Get context by id from database'''
        pass

    def find(self):
        '''Get all contexts from database'''
        pass

    def query(self, context_types=[], attribute_filters=[]):
        ''' Query contexts from database '''
        pass

    def clear(self):
        ''' clear all contexts '''
        pass

class MongoContextStore(ContextStore):
    '''MongoDB context store implementation'''

    def __init__(self, collection):
        self._collection = collection

    def store(self, context):
        if not isinstance(context, Context):
            raise TypeError('This is not a context object')

        return self._collection.insert_one(context.dict).inserted_id

    def find(self):
        return self._return_contexts(self._collection.find())

    def find_by_id(self, context_id):
        context_dict = self._collection.find_one({'_id': ObjectId(context_id)})
        return Context.from_dict(context_dict)

    def query(self, context_types=[], attribute_filters=[]):
        query = {}

        if len(context_types) > 0:
            query['$or'] = [{'contextType': context_type} for context_type in context_types]

        if len(attribute_filters) > 0:
            query['$and'] = [{'attributes.' + filter.key: filter.value} for filter in attribute_filters]

        return self._return_contexts(self._collection.find(query))


    def clear(self):
        self._collection.delete_many({})

    def _return_contexts(self, context_dicts):
        contexts = []
        for context_dict in context_dicts:
            contexts.append(Context.from_dict(context_dict))

        return contexts
