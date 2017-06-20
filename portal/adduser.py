#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    # Connect to the DB
    MONGO_ADDRESS = 'mongodb://testuser:testpassword@ds129342.mlab.com:29342/picompany_team2db'
    DB_NAME = 'picompany_team2db'
    collection  = MongoClient(MONGO_ADDRESS)[DB_NAME].users
    context_collection  = MongoClient(MONGO_ADDRESS)[DB_NAME].contexts

    # Ask for data to store
    user = raw_input("Enter your email: ")
    fullname = raw_input("Enter your fullname: ")
    department = raw_input("Enter your department: ")
    password = raw_input("Enter your password: ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    id = None

    # upsert based on user_name filter
    result = collection.update_one({"username": user}, {"$set": {"username": user, "fullname": fullname, "password": pass_hash, 'otp_secret': ''}}, True)
    id = result.upserted_id
    count = result.matched_count

    if(id is not None):
        print "New user created"
    else:
        print "Existing user updated"


    user = collection.find_one({"username": user})
    if user['_id'] is not None:
        context_collection.update_one({'_id': user['_id']}, {"$set":{'_id': user['_id'], "contextType": "medewerker", 'attributes': {"naam": fullname, "team": department}}}, True)



if __name__ == '__main__':
    main()
