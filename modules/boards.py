from sqlalchemy.sql import text
from flask import session
from db import db


def get_all_boards():
    sql = """SELECT * FROM boards WHERE is_city IS NULL"""
    result = db.session.execute(text(sql))
    boards = [dict(row._asdict()) for row in result]
    return boards


def new_board(header, lat, lon):
    sql = """INSERT INTO boards (header, pos_lat, pos_lon)
             VALUES (:header, :lat, :lon)"""
    db.session.execute(
        text(sql), {'header': header, 'lat': lat, 'lon': lon})
    db.session.commit()
