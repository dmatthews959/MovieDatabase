from flask import Blueprint, request, make_response, jsonify
from decorators import jwt_required, admin_required
import globals
from bson import ObjectId

movies_bp = Blueprint("movies_bp", __name__)

movies = globals.db.movieInfo

@movies_bp.route("/api/v1.0/movies", methods=["GET"])
def show_all_movies():
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))
    page_start = page_size * (page_num - 1)

    data_to_return = []
    for movie in movies.find().skip(page_start).limit(page_size):
        movie["_id"] = str(movie["_id"])

        if "reviews" in movie:
            for review in movie["reviews"]:
                if "_id" in review:
                    review["_id"] = str(review["_id"])

        data_to_return.append(movie)

    return make_response(jsonify(data_to_return), 200)



@movies_bp.route("/api/v1.0/movies/<string:id>", methods=["GET"])
def show_one_movie(id):
    movie = movies.find_one({"_id": ObjectId(id)})
    if movie is not None:
        movie["_id"] = str(movie["_id"])
        for review in movie["reviews"]:
            review["_id"] = str(review["_id"])
        return make_response(jsonify(movie), 200)
    else:
        return make_response(jsonify({"error": "Invalid Movie ID"}), 404)


@movies_bp.route("/api/v1.0/movies", methods=["POST"])
@jwt_required
def add_movie():
    if ("Title" in request.form and "Year" in request.form and "IMDb Rating" in request.form and "Runtime" in request.form and "Genre" in request.form and "Director" in request.form and "Actors" in request.form and "Plot" in request.form):
        new_movie = {
            "Title": request.form["Title"],
            "Year": request.form["Year"],
            "IMDb Rating": request.form["IMDb Rating"],
            "Runtime": request.form["Runtime"],
            "Genre": request.form["Genre"],
            "Director": request.form["Director"],
            "Actors": request.form["Actors"],
            "Plot": request.form["Plot"],
            "reviews": [],
        }
        new_movie_id = movies.insert_one(new_movie)
        new_movie_link = "http://localhost:5000/api/v1.0/movies/" + str(
            new_movie_id.inserted_id
        )
        return make_response(jsonify({"url": new_movie_link}), 201)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 404)


@movies_bp.route("/api/v1.0/movies/<string:id>", methods=["PUT"])
@jwt_required
def edit_movie(id):
    if ("Title" in request.form and "Year" in request.form and "IMDb Rating" in request.form and "Runtime" in request.form and "Genre" in request.form and "Director" in request.form and "Actors" in request.form and "Plot" in request.form):
        result = movies.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "Title": request.form["Title"],
                    "Year": request.form["Year"],
                    "IMDb Rating": request.form["IMDb Rating"],
                    "Runtime": request.form["Runtime"],
                    "Genre": request.form["Genre"],
                    "Director": request.form["Director"],
                    "Actors": request.form["Actors"],
                    "Plot": request.form["Plot"],
                    "reviews": [],
                }
            },
        )
        if result.matched_count == 1:
            edited_movie_link = "http://localhost:5000/api/v1.0/movies/" + id
            return make_response(jsonify({"url": edited_movie_link}), 200)
        else:
            return make_response(jsonify({"error": "Invalid movie ID"}), 404)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 404)


@movies_bp.route("/api/v1.0/movies/<string:id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_movie(id):
    result = movies.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid movie ID"}), 404)


@movies_bp.route("/api/v1.0/movies/title", methods=["GET"])
def search_movies():
    query = request.args.get("Title")
    if not query:
        return jsonify({"error": "Missing title parameter"}), 400

    data_to_return = []
    for movie in movies.find():
        title = movie.get("Title", "")
        if query.lower() in title.lower():
            movie["_id"] = str(movie["_id"])
            if "reviews" in movie:
                for review in movie["reviews"]:
                    if "_id" in review:
                        review["_id"] = str(review["_id"])
            data_to_return.append(movie)

    if not data_to_return:
        return make_response(jsonify({"error": "Invalid Title"}), 404)

    return make_response(jsonify(data_to_return), 200)


@movies_bp.route("/api/v1.0/movies/director", methods=["GET"])
def search_movies_by_director():
    director = request.args.get("Director")

    data_to_return = []
    for movie in movies.find():
        title = movie.get("Director", "")
        if director.lower() in title.lower():
            movie["_id"] = str(movie["_id"])
            if "reviews" in movie:
                for review in movie["reviews"]:
                    if "_id" in review:
                        review["_id"] = str(review["_id"])
            data_to_return.append(movie)

    if not data_to_return:
        return make_response(jsonify({"error": "Invalid Director"}), 404)

    return make_response(jsonify(data_to_return), 200)


@movies_bp.route("/api/v1.0/movies/searchyear", methods=["GET"])
def search_by_year():
    year = request.args.get("Year")
    results = movies.find({"Year": year})
    data_to_return = []

    for movie in results:
        movie["_id"] = str(movie["_id"])

        if "reviews" in movie:
            for review in movie["reviews"]:
                if "_id" in review:
                    review["_id"] = str(review["_id"])
        data_to_return.append(movie)

    if not data_to_return:
        return make_response(jsonify({"error": "Invalid Year"}), 404)

    return make_response(jsonify(data_to_return), 200)


@movies_bp.route("/api/v1.0/movies/year-range", methods=["GET"])
def movies_by_year_range():
    start = int(request.args.get("start"))
    end = int(request.args.get("end"))

    results = movies.find({"Year": {"$gte": start, "$lte": end}})

    data_to_return = []
    for movie in results:
        movie["_id"] = str(movie["_id"])

        if "reviews" in movie:
            for review in movie["reviews"]:
                if "_id" in review:
                    review["_id"] = str(review["_id"])
        data_to_return.append(movie)

    if not data_to_return:
        return make_response(jsonify({"error": "Invalid Start and End Dates"}), 404)

    return make_response(jsonify(data_to_return), 200)


@movies_bp.route("/api/v1.0/movies/genre", methods=["GET"])
def movies_by_genre():
    genre = request.args.get("Genre")
    genre = genre.lower()
    results = movies.find()

    data_to_return = []
    for movie in results:
        genre_field = movie.get("Genre", "")
        genre_list = genre_field.lower().split(",")

        if genre in [genre.replace(" ", "") for genre in genre_list]:
            movie["_id"] = str(movie["_id"])

            if "reviews" in movie:
                for review in movie["reviews"]:
                    if "_id" in review:
                        review["_id"] = str(review["_id"])

            data_to_return.append(movie)

    if not data_to_return:
        return make_response(jsonify({"error": "No Genres were found"}), 404)

    return make_response(jsonify(data_to_return), 200)


@movies_bp.route("/api/v1.0/movies/minrating/<float:minrating>", methods=["GET"])
def showMoviesAboveMinRating(minrating):
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))
    page_start = page_size * (page_num - 1)

    data_to_return = []
    for movie in (
        movies.find({"IMDb Rating": {"$gte": minrating}}).skip(page_start).limit(page_size)
    ):
        movie["_id"] = str(movie["_id"])
        if "reviews" in movie:
            for review in movie["reviews"]:
                if "_id" in review:
                    review["_id"] = str(review["_id"])
        data_to_return.append(movie)

    if not data_to_return:
        return make_response(
            jsonify(
                {
                    "error": "No movies were found with a rating more than or equal to " + str(minrating)
                }
            ),
            404,
        )

    return make_response(jsonify(data_to_return), 200)


@movies_bp.route("/api/v1.0/movies/by-actor/<actor_name>", methods=["GET"])
def movies_by_actor(actor_name):
    query = {
        "$expr": {
            "$in": [
                actor_name.lower(),
                {
                    "$map": {
                        "input": {"$split": ["$Actors", ", "]},
                        "as": "actor",
                        "in": {"$toLower": "$$actor"},
                    }
                },
            ]
        }
    }
    projection = {"_id": 0, "Title": 1, "Actors": 1}
    results = list(movies.find(query, projection))
    return make_response(jsonify(results), 200)