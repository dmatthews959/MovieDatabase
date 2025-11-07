from flask import Blueprint, request, make_response, jsonify
from decorators import jwt_required, admin_required
from bson import ObjectId
import globals

reviews_bp = Blueprint("reviews_bp", __name__)

movies = globals.db.movieInfo


@reviews_bp.route("/api/v1.0/movies/<string:id>/reviews", methods=["POST"])
@jwt_required
def add_new_review(id):
    new_review = {
        "_id": ObjectId(),
        "username": request.form["username"],
        "comment": request.form["comment"],
        "stars": request.form["stars"],
    }
    result = movies.update_one(
        {"_id": ObjectId(id)}, {"$push": {"reviews": new_review}}
    )
    if result.matched_count == 1:
        new_review_link = ("http://localhost:5000/api/v1.0/movies/" + id + "/reviews/" + str(new_review["_id"]))
        return make_response(jsonify({"url": new_review_link}), 201)
    else:
        return make_response(jsonify({"error": "Invalid movie ID"}), 404)


@reviews_bp.route("/api/v1.0/movies/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    data_to_return = []
    movie = movies.find_one({"_id": ObjectId(id)}, {"reviews": 1, "_id": 0})
    for review in movie["reviews"]:
        review["_id"] = str(review["_id"])
        data_to_return.append(review)
    return make_response(jsonify(data_to_return), 200)


@reviews_bp.route("/api/v1.0/movies/<mid>/reviews/<rid>", methods=["GET"])
def fetch_one_review(mid, rid):
    movie = movies.find_one({"reviews._id": ObjectId(rid)}, {"_id": 0, "reviews.$": 1})
    if movie is None:
        return make_response(jsonify({"error": "Invalid movie ID or review ID"}), 404)
    movie["reviews"][0]["_id"] = str(movie["reviews"][0]["_id"])
    return make_response(jsonify(movie["reviews"][0]), 200)


@reviews_bp.route("/api/v1.0/movies/<mid>/reviews/<rid>", methods=["PUT"])
@jwt_required
def edit_review(mid, rid):
    edited_review = {
        "reviews.$.username": request.form["username"],
        "reviews.$.comment": request.form["comment"],
        "reviews.$.stars": request.form["stars"],
    }
    movies.update_one({"reviews._id": ObjectId(rid)}, {"$set": edited_review})
    edit_review_url = "http://localhost:5000/api/v1.0/movies/" + mid + "/reviews/" + rid
    return make_response(jsonify({"url": edit_review_url}), 200)


@reviews_bp.route("/api/v1.0/movies/<mid>/reviews/<id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_review(mid, rid):
    movies.update_one(
        {"_id": ObjectId(mid)}, {"$pull": {"reviews": {"_id": ObjectId(rid)}}}
    )
    return make_response(jsonify({}), 204)

@reviews_bp.route("/api/v1.0/movies/<mid>/reviews/stars", methods=["GET"])
def movie_name_and_stars(mid):
    stars = request.args.get("stars")
    if not stars:
        return jsonify({"error": "Missing stars parameter"}), 400

    movie = movies.find_one({"_id": ObjectId(mid)})

    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    if "_id" in movie:
        movie["_id"] = str(movie["_id"])

    if "reviews" in movie:
        for review in movie["reviews"]:
            if "_id" in review:
                review["_id"] = str(review["_id"])
        movie["reviews"] = [
            review
            for review in movie["reviews"]
            if "stars" in review and str(review["stars"]) == str(stars)
        ]

    return make_response(jsonify(movie), 200)


@reviews_bp.route("/api/v1.0/movies/reviewed_by/<string:username>", methods=["GET"])
def show_movies_reviewed_by_user(username):
    pipeline = [{"$match": {"reviews": {"$elemMatch": {"username": username}}}}]
    data_to_return = []
    for movie in movies.aggregate(pipeline):
        movie["_id"] = str(movie["_id"])
        for review in movie["reviews"]:
            review["_id"] = str(review["_id"])
        data_to_return.append(movie)

    if not data_to_return:
        return make_response(jsonify({"error": "No reviews for user " + username}), 404)

    return make_response(jsonify(data_to_return), 200)