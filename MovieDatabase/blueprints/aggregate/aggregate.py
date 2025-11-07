from flask import Blueprint, jsonify, make_response
import globals

aggregate_bp = Blueprint("aggregate_bp", __name__)

movies = globals.db.movieInfo


@aggregate_bp.route("/api/v1.0/movies/genre-count", methods=["GET"])
def genre_count():
    pipeline = [
        {
            "$addFields": {
                "genreArray": {
                    "$split": [
                        "$Genre",
                        ", ",
                    ]  # Split the Array into each individual Genre
                }
            }
        },
        {"$unwind": "$genreArray"},
        {"$group": {"_id": "$genreArray", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "genre": "$_id", "count": 1}},
        {"$sort": {"count": -1}},
    ]
    results = list(movies.aggregate(pipeline))
    return make_response(jsonify(results), 200)


@aggregate_bp.route("/api/v1.0/movies/director-count", methods=["GET"])
def director_count():
    pipeline = [
        {
            "$addFields": {
                "directorArray": {
                    "$split": [
                        "$Director",
                        ", ",
                    ]  # Split the Array into each Individual Director
                }
            }
        },
        {"$unwind": "$directorArray"},
        {"$group": {"_id": "$directorArray", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "director": "$_id", "count": 1}},
        {"$sort": {"count": -1}},
    ]
    results = list(movies.aggregate(pipeline))
    return make_response(jsonify(results), 200)


@aggregate_bp.route("/api/v1.0/movies/actor-count", methods=["GET"])
def actor_count():
    pipeline = [
        {"$addFields": {"actorArray": {"$split": ["$Actors", ", "]}}},
        {"$unwind": "$actorArray"},
        {"$group": {"_id": "$actorArray", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "actor": "$_id", "count": 1}},
        {"$sort": {"count": -1}},
    ]
    results = list(movies.aggregate(pipeline))
    return make_response(jsonify(results), 200)


@aggregate_bp.route("/api/v1.0/movies/average-review-rating", methods=["GET"])
def average_review_rating():
    pipeline = [
        {"$unwind": "$reviews"},
        {"$addFields": {"numericStars": {"$toDouble": "$reviews.stars"}}},
        {"$group": {"_id": "$Title", "averageReviewRating": {"$avg": "$numericStars"}}},
        {"$project": {"_id": 0, "Title": "$_id", "averageReviewRating": 1}},
    ]
    results = list(movies.aggregate(pipeline))
    return make_response(jsonify(results), 200)