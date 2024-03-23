import random
import string

from flask import request, session, abort
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
        return boards_module.get_all_boards()
    if request.method == "POST":
        if not request.form["lat"]:
            abort(400)
        header = request.form["header"]
        lat = request.form["lat"]
        lon = request.form["lon"]
        boards_module.new_board(header, lat, lon)


@app.route("/boards/<int:board_id>", methods=["GET", "POST"])
def board(board_id):
    if request.method == "GET":
        board_info = boards_module.get_board_by_id(board_id)
        content = boards_module.get_posts_by_board_id(board_id)
        for post in content:
            content[post["post_id"]] = posts_module.get_post_by_id(
                post["post_id"])
        board_info["posts"] = content
        return board_info
    if request.method == "POST":
        header = request.form["header"]
        content = request.form["content"]
        pos_lat = request.form["lat"]
        pos_lon = request.form["lon"]
        if not (pos_lat and pos_lon):
            posts_module.new_post(board_id, header, content)
        else:
            posts_module.new_post(board_id, header, content, pos_lat, pos_lon)


@app.route("/boards/<int:board_id>/<int:post_id>", methods=["GET", "POST"])
def post(board_id, post_id):
    if request.method == "GET":
        content = posts_module.get_post_by_id(post_id)
        content["votes"] = votes_module.get_votes_by_post_id(post_id)
        content["voted"] = votes_module.if_voted(post_id)
        return content


@app.route("/boards/<int:board_id>/<int:post_id>/vote", methods=["GET", "POST"])
def votes(board_id, post_id):
    if request.method == "GET":
        return str(votes_module.get_votes_by_post_id(post_id))
    if request.method == "POST":
        votes_module.vote_post(post_id)


@app.route("/boards/<int:board_id>/<int:post_id>/comments")
def comments(board_id, post_id):
    return "COMMENTTI"


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return users_module.get_all_users()
    if request.method == "POST":
        username = request.form["username"]
        password = request
        birth_year = request.form["birth_year"]
        home_lat = request.form["home_lat"]
        home_lon = request.form["home_lon"]
        gender = request.form["gender"]
        users_module.new_users(username, password, birth_year,
                               home_lat, home_lon, gender)


@app.route("/login", methods=["POST"])
def login():
    '''RETURNS TRUE OR FALSE BASED ON SUCCESS (as string lol)'''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return str(users_module.login(username, password))
    return "HEIPULIS! TÄMÄ METODI OTTAA VAAN POSTAUKSIA"
