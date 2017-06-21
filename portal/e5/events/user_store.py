
'''Userstore module'''
from e5.events import Context
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash


class UserStore(object):
    '''Contextstore interface'''
    def store(self, full_name, username, password):
        '''Store an event in the evenstore'''
        pass

class MongoUserStore(UserStore):
    '''MongoDB user store implementation'''

    def __init__(self, collection):
        self._collection = collection

    def store(self, full_name, username, password):
        pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
        return self._collection.update_one(
            {"username": username},
            {"$set": {"username": username, "fullname": full_name, "password": pass_hash, 'otp_secret': ''}}
            , True
        ).upserted_id
