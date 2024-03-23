import random
import string

from flask import request, session, abort, jsonify
from app import app
import modules.boards as boards_module
import modules.users as users_module
import modules.posts as posts_module
import modules.votes as votes_module


@app.route("/")
def index():
    random_string = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(10))
    users_module.new_users(random_string, random_string, 1, 1, 1, "MAN")
    boards_module.new_board(random_string, 1, 1)
    b = boards_module.get_all_boards()[0]["board_id"]
    print(b)
    session["user_id"] = 2
    posts_module.new_post(b, random_string, random_string + random_string)
    votes_module.vote_post(1)

    return "haha"


@app.route("/boards", methods=["GET", "POST"])
def boards():
    if request.method == "GET":
        return jsonify(boards_module.get_all_boards())
    if request.method == "POST":
        data = request.get_json()
        if not data.get("lat"):
            abort(400)
        header = data["header"]
        lat = data["lat"]
        lon = data["lon"]
        boards_module.new_board(header, lat, lon)
        return jsonify({"message": "Board created successfully."})


@app.route("/boards/<int:board_id>", methods=["GET", "POST"])
def board(board_id):
    if request.method == "GET":
        board_info = boards_module.get_board_by_id(board_id)
        content = boards_module.get_posts_by_board_id(board_id)
        for post in content:
            content[post["post_id"]] = posts_module.get_post_by_id(
                post["post_id"])
        board_info["posts"] = content
        return jsonify(board_info)
    if request.method == "POST":
        data = request.get_json()
        header = data["header"]
        content = data["content"]
        pos_lat = data.get("lat")
        pos_lon = data.get("lon")
        if not (pos_lat and pos_lon):
            posts_module.new_post(board_id, header, content)
        else:
            posts_module.new_post(board_id, header, content, pos_lat, pos_lon)
        return jsonify({"message": "Post created successfully."})


@app.route("/boards/<int:board_id>/<int:post_id>", methods=["GET", "POST"])
def post(board_id, post_id):
    if request.method == "GET":
        content = posts_module.get_post_by_id(post_id)
        return jsonify(content)


@app.route("/boards/<int:board_id>/<int:post_id>/vote", methods=["GET", "POST"])
def votes(board_id, post_id):
    if request.method == "GET":
        return str(votes_module.get_votes_by_post_id(post_id))
    if request.method == "POST":
        votes_module.vote_post(post_id)
        return jsonify({"message": "Vote recorded successfully."})


@app.route("/boards/<int:board_id>/<int:post_id>/comments")
def comments(board_id, post_id):
    return "COMMENTTI"


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return jsonify(users_module.get_all_users())
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        birth_year = data["birth_year"]
        home_lat = data["home_lat"]
        home_lon = data["home_lon"]
        gender = data["gender"]
        users_module.new_users(username, password, birth_year,
                               home_lat, home_lon, gender)
        return jsonify({"message": "User created successfully."})


@app.route("/login", methods=["POST"])
def login():
    '''RETURNS TRUE OR FALSE BASED ON SUCCESS (as string lol)'''
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        return str(users_module.login(username, password))
    return "HEIPULIS! TÄMÄ METODI OTTAA VAAN POSTAUKSIA"
