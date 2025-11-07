from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.8")
db = client.Movies
movies = db.movieInfo
awards = db.awards

award_data = [
    {
        "title": "Oppenheimer",
        "award_name": "Academy Award",
        "category": "Best Picture",
        "year": 2023,
        "won": True
    },
]

for award in award_data:
    movie = movies.find_one({"Title": award["title"]})
    if movie:
        awards.insert_one({
            "movie_id": movie["_id"],
            "award_name": award["award_name"],
            "category": award["category"],
            "year": award["year"],
            "won": award["won"]
        })
    else:
        print(f"Movie not found: {award['title']}")