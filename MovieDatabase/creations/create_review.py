import random
from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.8")
db = client.Movies
movies = db.movieInfo

# Sample data
usernames = ["Declan", "MovieBuff42", "CineFan", "CritiqueMaster", "PopcornLover"]
comments = [
    "Absolutely loved it!",
    "Could've been better.",
    "Stunning visuals and great acting.",
    "Not my cup of tea.",
    "A masterpiece of storytelling.",
    "Too long, but worth it.",
    "Great soundtrack and pacing.",
    "Felt a bit rushed.",
    "Oscar-worthy performance!",
    "I’d watch it again."
]

def generate_review():
    return {
        "_id": ObjectId(),  # 👈 Unique ID for each review
        "username": random.choice(usernames),
        "comment": random.choice(comments),
        "stars": random.randint(1, 5)
    }

def add_reviews_to_random_movies(review_count=5, movie_count=3):
    movie_list = list(movies.find())
    if not movie_list:
        print("No movies found in the database.")
        return

    selected_movies = random.sample(movie_list, min(movie_count, len(movie_list)))
    for movie in selected_movies:
        reviews = [generate_review() for _ in range(review_count)]
        movies.update_one(
            { "_id": movie["_id"] },
            { "$push": { "reviews": { "$each": reviews } } }
        )
        print(f"Added {review_count} reviews to '{movie['Title']}'")

# Example usage
add_reviews_to_random_movies(review_count=5, movie_count=3)