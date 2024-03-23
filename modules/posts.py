from sqlalchemy.sql import text
from flask import session
from db import db


def new_post(board_id, header, content, pos_lat=None, pos_lon=None):
    owner_id = session["user_id"]
    if not (board_id or (pos_lat and pos_lon)):
        return False
    sql = """INSERT INTO posts (owner_id, board_id, header, content, pos_lat, pos_lon, timestamp)
             VALUES (:owner_id, :board_id, :header, :content, :pos_lat, :pos_lon, NOW())"""
    db.session.execute(text(sql), {'owner_id': owner_id, 'board_id': board_id,
                       'header': header, 'content': content, 'pos_lat': pos_lat, 'pos_lon': pos_lon})
    db.session.commit()


def get_post_by_id(id):
    user_id = session["user_id"]
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
    post = result.fetchone()._asdict()
    return post
