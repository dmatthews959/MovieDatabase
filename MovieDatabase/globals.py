from pymongo import MongoClient

secret_key = 'movieinfodatabasesecretkey'

client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.8")
db = client.Movies