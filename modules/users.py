from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db

data_keys = ["user_id", "username", "password", "birth_year",
             "home_lat", "home_lon", "gender", "is_admin"]


def get_all_users():
    sql = """SELECT * FROM users"""
    result = db.session.execute(text(sql)).all()
    users = [dict(row._asdict()) for row in result]
    return users


def get_user_by_id(id):
    if not id:
        return False
    sql = """SELECT * FROM users WHERE user_id = :id"""
    result = db.session.execute(text(sql), {'id': id})
    return result.fetchone()[0]


def new_users(username, password, birth_year, home_lat, home_lon, gender):
    hashed_password = generate_password_hash(password)
    sql = """INSERT INTO users (username, password, birth_year, home_lat, home_lon, gender)
             VALUES (:username, :password, :birth_year, :home_lat, :home_lon, :gender)"""
    db.session.execute(text(sql), {'username': username, 'password': hashed_password,
                       'birth_year': birth_year, 'home_lat': home_lat, 'home_lon': home_lon, 'gender': gender})
    db.session.commit()


def login(username, password):
    sql = """SELECT * FROM users WHERE username == :username"""
    result = db.session.execute(text(sql), {'username': username})
    user = result.fetchone()
    if not user:
        return False
    hashed_password = user.password
    if check_password_hash(hashed_password, password):
        session['username'] = user.username
        session['user_id'] = user.user_id
        session['is_admin'] = user.is_admin is True
        return True
    return False
