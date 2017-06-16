import os

from pymongo import MongoClient
from datetime import timedelta

WTF_CSRF_ENABLED = True
DB_NAME = ''
SECRET_KEY = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
MONGO_ADDRESS = ''

DATABASE = MongoClient(MONGO_ADDRESS)[DB_NAME]
EVENTS_COLLECTION = DATABASE.events
USER_COLLECTION = DATABASE.users
CONTEXTS_COLLECTION = DATABASE.contexts
SETTINGS_COLLECTION = DATABASE.settings

JWT_EXPIRATION_DELTA = timedelta(days=1000)

DEBUG = True