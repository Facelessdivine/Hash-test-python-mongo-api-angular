from flask_pymongo import pymongo
import os

from  dotenv import load_dotenv
load_dotenv(override=True)
# USER = os.getenv('DB_USER')
# PASSWORD = os.getenv('DB_PASSWORD')
# HOST = os.getenv('DB_HOST')
# NAME = os.getenv('DB_NAME')
# URI = os.getenv('DB_URI')
# client = pymongo.MongoClient(f'mongodb+srv://{USER}:{PASSWORD}@{HOST}.mongodb.net/{NAME}?retryWrites=true')
client = pymongo.MongoClient('mongodb://localhost:27017')
# print('hola conecte la base de datos')
db_users = client.users