import random
import string

from flask import redirect, render_template, request, session, abort
from app import app
import modules.boards as boards_module
import modules.users as users_module
import modules.posts as posts_module


@app.route("/")
def index():
    random_string = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(10))
    users_module.new_users(random_string, random_string, 1, 1, 1, "MAN")
    boards_module.new_board(random_string, 1, 1)
    b = boards_module.get_all_boards()[0]["board_id"]
    print(b)
    session["user_id"] = 1
    posts_module.new_post(b, random_string, random_string + random_string)

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
def board_by_id(board_id):
    if request.method == "GET":
        board_info = boards_module.get_board_by_id(board_id)
        content = boards_module.get_posts_by_board_id(board_id)
        board_info["posts"] = content
        return board_info


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
