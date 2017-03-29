from flask_pymongo import PyMongo
import os

MONGO_DBNAME = 'classadmin'
MONGO_URI = 'mongodb://localhost:27017/classadmin'
MONGO_USERNAME = ''
MONGO_PASSWORD = ''

# The global connection object which will be shared
mongo = None

def setup_mongo_connection(app):
	global mongo

	MONGO_URL = os.environ.get('MONGO_URL')
	if not MONGO_URL:
		MONGO_URL = MONGO_URI;

	app.config['MONGO_DBNAME'] = MONGO_DBNAME
	app.config['MONGO_URI'] = MONGO_URL
	app.config['MONGO_USERNAME'] = MONGO_USERNAME
	app.config['MONGO_PASSWORD'] = MONGO_PASSWORD

	mongo = PyMongo(app)
