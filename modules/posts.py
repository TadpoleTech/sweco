from sqlalchemy.sql import text
from osm_functions import query
from flask import session
from db import db


def new_post(header, content, owner_id, board_id=None, pos_lat=None, pos_lon=None):
    if not (board_id or (pos_lat and pos_lon)):
        return False
    if pos_lat and pos_lon:
        address_data = query(pos_lon, pos_lat)["addressparts"]
        city = address_data["city"]
        suburb = address_data["suburb"]
    else:
        city = None
        suburb = None
    sql = """INSERT INTO posts (owner_id, board_id, header, content, pos_lat, pos_lon, city, suburb timestamp)
             VALUES (:owner_id, :board_id, :header, :content, :pos_lat, :pos_lon, :city, :suburb, NOW())"""
    db.session.execute(text(sql), {'owner_id': owner_id, 'board_id': board_id,
                       'header': header, 'content': content, 'pos_lat': pos_lat, 'pos_lon': pos_lon,
                                   'city': city, 'suburb': suburb})
    db.session.commit()


def get_post_by_id(id, user_id=None):
    if user_id:
        sql = """SELECT posts.*,
                SUM(CASE when posts.post_id = votes.post_id THEN 1 ELSE 0 END) AS vote_count,
                SUM(CASE WHEN posts.post_id = votes.post_id AND votes.user_id = :user_id 
                THEN 1 ELSE 0 END) AS has_voted
                FROM posts
                LEFT JOIN votes ON votes.post_id = posts.post_id
                WHERE posts.post_id = :id
                GROUP BY posts.post_id
            """
        result = db.session.execute(text(sql), {'id': id, 'user_id': user_id})
    else:
        sql = """SELECT posts.*,
                SUM(CASE when posts.post_id = votes.post_id THEN 1 ELSE 0 END) AS vote_count
                FROM posts
                LEFT JOIN votes ON votes.post_id = posts.post_id
                WHERE posts.post_id = :id
                GROUP BY posts.post_id"""
        result = db.session.execute(text(sql), {'id': id})
    post = result.fetchone()._asdict()
    return post


def get_city_posts(user_id=None, city=None):
    if user_id:
        sql = """SELECT posts.*,
                SUM(CASE when posts.post_id = votes.post_id THEN 1 ELSE 0 END) AS vote_count,
                SUM(CASE WHEN posts.post_id = votes.post_id AND votes.user_id = :user_id 
                THEN 1 ELSE 0 END) AS has_voted
                FROM posts
                LEFT JOIN votes ON votes.post_id = posts.post_id
                WHERE city = :city
                GROUP BY posts.post_id
            """
        result = db.session.execute(
            text(sql), {'user_id': user_id, 'city': city}).fetchall()
    else:
        sql = """SELECT posts.*,
                SUM(CASE when posts.post_id = votes.post_id THEN 1 ELSE 0 END) AS vote_count
                FROM posts
                LEFT JOIN votes ON votes.post_id = posts.post_id
                WHERE city = :city
                GROUP BY posts.post_id"""
        result = db.session.execute(text(sql), {'city': city}).fetchall()
    posts = [dict(row._asdict()) for row in result]
    return posts


def get_suburb_posts(user_id=None, suburb=None):
    if user_id:
        sql = """SELECT posts.*,
                SUM(CASE when posts.post_id = votes.post_id THEN 1 ELSE 0 END) AS vote_count,
                SUM(CASE WHEN posts.post_id = votes.post_id AND votes.user_id = :user_id 
                THEN 1 ELSE 0 END) AS has_voted
                FROM posts
                LEFT JOIN votes ON votes.post_id = posts.post_id
                WHERE suburb = :suburb
                GROUP BY posts.post_id
            """
        result = db.session.execute(
            text(sql), {'user_id': user_id, 'suburb': suburb}).fetchall()
    else:
        sql = """SELECT posts.*,
                SUM(CASE when posts.post_id = votes.post_id THEN 1 ELSE 0 END) AS vote_count
                FROM posts
                LEFT JOIN votes ON votes.post_id = posts.post_id
                WHERE city = :city
                GROUP BY posts.post_id"""
        result = db.session.execute(text(sql), {'city': city}).fetchall()
    posts = [dict(row._asdict()) for row in result]
    return posts
