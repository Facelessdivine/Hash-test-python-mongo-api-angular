from flask_pymongo import pymongo
import os
from  dotenv import load_dotenv
load_dotenv(override=True)
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
NAME = os.getenv('DB_NAME')
client = pymongo.MongoClient(f'mongodb+srv://{USER}:{PASSWORD}@{HOST}.mongodb.net/{NAME}?retryWrites=true')
c_users = client.users