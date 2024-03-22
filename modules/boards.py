from sqlalchemy.sql import text
from flask import session
from db import db


def get_all_boards():
    sql = """SELECT * FROM boards"""
    result = db.session.execute(text(sql)).fetchall()
    boards = [dict(row._asdict()) for row in result]
    return boards


def new_board(header, lat, lon):
    sql = """INSERT INTO boards (header, pos_lat, pos_lon)
             VALUES (:header, :lat, :lon)"""
    db.session.execute(
        text(sql), {'header': header, 'lat': lat, 'lon': lon})
    db.session.commit()


def get_board_by_id(id):
    sql = """SELECT * FROM boards WHERE board_id = :board_id"""
    result = db.session.execute(text(sql), {'board_id': id}).fetchone()
    board = dict(result._asdict())
    return board


def get_posts_by_board_id(id):
    sql = """SELECT * FROM posts WHERE board_id = :board_id"""
    result = db.session.execute(text(sql), {'board_id': id}).fetchall()
    posts = [dict(row._asdict()) for row in result]
    return posts
