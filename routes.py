import random
import string

from flask import request, session, abort, jsonify
from app import app
import modules.boards as boards_module
import modules.users as users_module
import modules.posts as posts_module
import modules.votes as votes_module
import modules.comments as comments_module
import modules.osm_functions as osm_functions


def get_user_id():
    if "user_id" in session:
        return session["user_id"]
    return None


def is_admin():
    if "is_admin" in session:
        return session["is_admin"]
    return False


@app.route("/")
def index():
    random_string = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(10))
    users_module.new_users(random_string, random_string, 1, 1, 1, "MAN")
    session["user_id"] = 1

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
    user_id = get_user_id()
    if request.method == "GET":
        board_info = boards_module.get_board_by_id(board_id)
        content = boards_module.get_posts_by_board_id(board_id)
        content_dict = {}
        for post in content:
            content_dict[post["post_id"]] = posts_module.get_post_by_id(
                post["post_id"], user_id=user_id)
        board_info["posts"] = content_dict
        return jsonify(board_info)
    if request.method == "POST":
        data = request.get_json()
        header = data["header"]
        content = data["content"]
        pos_lat = data.get("lat")
        pos_lon = data.get("lon")
        if not (pos_lat and pos_lon):
            posts_module.new_post(
                owner_id=user_id, header=header, content=content, board_id=board_id)
        else:
            posts_module.new_post(owner_id=user_id, header=header,
                                  content=content, pos_lat=pos_lat, pos_lon=pos_lon)
        return jsonify({"message": "Post created successfully."})


@app.route("/boards/<int:board_id>/<int:post_id>", methods=["GET", "POST"])
def post(board_id, post_id):
    user_id = get_user_id()
    if request.method == "GET":
        content = posts_module.get_post_by_id(id=post_id, user_id=user_id)
        return jsonify(content)


@app.route("/boards/<int:board_id>/<int:post_id>/vote", methods=["GET", "POST"])
def votes(board_id, post_id):
    user_id = get_user_id()
    if request.method == "GET":
        return str(votes_module.get_votes_by_post_id(id=post_id))
    if request.method == "POST":
        if user_id:
            votes_module.vote_post(post_id=post_id, user_id=user_id)
            return jsonify({"message": "Vote recorded successfully."})
        abort(401)


@app.route("/boards/<int:board_id>/<int:post_id>/comments", methods=["GET", "POST"])
def comments(board_id, post_id):
    if request.method == "GET":
        return jsonify(comments_module.get_comments_by_post_id(post_id))
    if request.method == "POST":
        if not is_admin():
            abort(403)
        if not get_user_id():
            abort(401)
        data = request.get_json()
        content = data["content"]
        user_id = get_user_id()
        comments_module.new_comment(
            post_id=post_id, user_id=user_id, content=content)
        return jsonify({"message": "Comment created successfully."})


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
        if users_module.login(username, password):
            return jsonify({"message": "Login successful."})
        return jsonify({"message": "Login failed."})
    return "HEIPULIS! TÄMÄ METODI OTTAA VAAN POSTAUKSIA"


@app.route("/logout")
def logout():
    session["user_id"] = None
    session["username"] = None
    session["is_admin"] = None


@app.route("/current_user")
def current_user():
    return jsonify(users_module.get_user_by_id(get_user_id()))


@app.route("/posts", methods=["POST"])
def new_post():
    user_id = get_user_id()
    if not user_id:
        abort(401)
    if request.method == "POST":
        data = request.get_json()
        header = data["header"]
        content = data["content"]
        post_lat = data["pos_lat"]
        pos_lon = data["pos_lon"]
        posts_module.new_post(header=header, content=content,
                              owner_id=user_id, pos_lat=post_lat, pos_lon=pos_lon)
        return jsonify({"message": "Post created successfully."})


@app.route("/posts/city/<cityname>", methods=["GET"])
def posts_city(cityname):
    user_id = get_user_id()
    if request.method == "GET":
        content = posts_module.get_city_posts(user_id=user_id, city=cityname)
        return jsonify(content)


@app.route("/posts/city/<cityname>/<suburb>", methods=["GET", "POST"])
def posts_suburb(cityname, suburb):
    user_id = get_user_id()
    if request.method == "GET":
        content = posts_module.get_suburb_posts(user_id=user_id, suburb=suburb)
        return jsonify(content)


@app.route("/users/<int:user_id>/toggle_admin", methods=["GET"])
def tgl_admin_privs(user_id):
    if not is_admin():
        abort(403)
    users_module.toggle_admin_privs(user_id)
    return jsonify({"message": "Admin privileges toggled."})


@app.route("/get_current_address_info", methods=["POST"])
def get_current_address_info():
    if request.method == "POST":
        data = request.get_json()
        lat = data["lat"]
        lon = data["lon"]
        address_data = osm_functions.query(lat, lon)["addressparts"]
        return jsonify({'city': address_data["city"], 'suburb': address_data['suburb']})
