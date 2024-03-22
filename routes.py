from flask import redirect, render_template, request, session, abort
from app import app
import modules.boards as boards_module
import modules.users as users_module


@app.route("/")
def index():
    boards_module.new_board(0, "kaka", 1, 1)

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

@app.route("/boards/<int:board_id>")
def board_or_country_id(board_id):
    


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
