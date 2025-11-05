from pymongo import MongoClient
import random

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Movies
movies = db.movieInfo

for movie in movies.find():
    movies.update_one(
        { "_id" : movie['_id'] },
        { 
            "$set" : { 
                "reviews" : [],
            } 
        }
    )
