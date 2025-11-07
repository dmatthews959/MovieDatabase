from flask import Blueprint, jsonify, make_response, request
import globals
from decorators import jwt_required, admin_required
from bson import ObjectId

awards_bp = Blueprint("awards_bp", __name__)

movies = globals.db.movieInfo
awards = globals.db.awards


@awards_bp.route("/api/v1.0/awards/all", methods=["GET"])
def get_all_awards():
    data_to_return = []
    for award in awards.find():
        award["_id"] = str(award["_id"])
        award["movie_id"] = str(award["movie_id"])
        data_to_return.append(award)
    return make_response(jsonify(data_to_return), 200)


@awards_bp.route("/api/v1.0/movies/<movie_id>/awards", methods=["GET"])
def get_awards_for_movie(movie_id):
    data_to_return = []
    for award in awards.find({"movie_id": ObjectId(movie_id)}):
        award["_id"] = str(award["_id"])
        award["movie_id"] = str(award["movie_id"])
        data_to_return.append(award)
    if not data_to_return:
        return make_response(jsonify({"error": "No awards found for this movie"}), 404)
    return make_response(jsonify(data_to_return), 200)


@awards_bp.route("/api/v1.0/awards/<int:year>/winners", methods=["GET"])
def get_award_winners_by_year(year):
    data_to_return = []
    for award in awards.find({"year": year, "won": True}):
        award["_id"] = str(award["_id"])
        award["movie_id"] = str(award["movie_id"])
        data_to_return.append(award)
    if not data_to_return:
        return make_response(
            jsonify({"error": "No award winners found for year " + str(year)}), 404
        )
    return make_response(jsonify(data_to_return), 200)


@awards_bp.route("/api/v1.0/awards/add", methods=["POST"])
@jwt_required
def add_award():
    data = request.get_json()
    if not data or "title" not in data:
        return make_response(jsonify({"error": "Missing form data"}), 404)

    movie = movies.find_one({"Title": data["title"]})
    if not movie:
        return make_response(jsonify({"error": "Movie not found in database"}), 400)

    new_award = {
        "movie_id": movie["_id"],
        "award_name": data["award_name"],
        "category": data["category"],
        "year": data["year"],
        "won": data["won"],
    }

    result = awards.insert_one(new_award)
    new_award_link = "http://localhost:5000/api/v1.0/awards/" + str(result.inserted_id)
    return make_response(jsonify({"url": new_award_link}), 201)


@awards_bp.route("/api/v1.0/awards/<string:id>", methods=["PUT"])
@jwt_required
def edit_award(id):
    if (
        "award_name" in request.form and "category" in request.form and "year" in request.form and "won" in request.form and "movie_id" in request.form):
        result = awards.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "award_name": request.form["award_name"],
                    "category": request.form["category"],
                    "year": int(request.form["year"]),
                    "won": request.form["won"].lower == "true",
                    "movie_id": ObjectId(request.form["movie_id"]),
                }
            },
        )
        if result.matched_count == 1:
            edited_award_link = "http://localhost:5000/api/v1.0/awards/" + id
            return make_response(jsonify({"url": edited_award_link}), 200)
        else:
            return make_response(jsonify({"error": "Invalid award ID"}), 404)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 404)


@awards_bp.route("/api/v1.0/awards/<string:id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_award(id):
    result = awards.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid award ID"}), 404)


@awards_bp.route("/api/v1.0/awards/awardcompany/<string:award_name>", methods=["GET"])
def get_awards_by_award_name(award_name):
    data_to_return = []
    for award in awards.find({"award_name": award_name}):
        award["_id"] = str(award["_id"])
        award["movie_id"] = str(award["movie_id"])
        data_to_return.append(award)
    if not data_to_return:
        return make_response(
            jsonify({"error": f"No awards found in award_name '{award_name}'"}), 404
        )
    return make_response(jsonify(data_to_return), 200)