To install the server do the following:

1. Create an account at mlab.com
2. Create a database at mlab.com
3. Open config.py and set the MONGO_ADDRESS and DB_NAME
4. Open adduser.py and set the MONGO_ADDRESS and DB_NAME
5. Make sure that virtualenv is installed and run $ virtualenv env
6. Run $ source env/bin/activate
7. Run $ pip install -r requirements.txt
8. Create users by running $ python adduser.py
9. To run the server $ python server.py
10. Login using your created credentials
