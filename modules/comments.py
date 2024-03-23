from sqlalchemy.sql import text
from db import db


def get_comments_by_post_id(id):
    sql = """SELECT * FROM comments WHERE post_id == :id"""
    result = db.session.execute(text(sql), {'id': id}).fetchall()
    comments = [dict(row._asdict()) for row in result]
    return comments


def new_comment(post_id, user_id, content):
    sql = """INSERT INTO comments (post_id, user_id, content, timestamp)
             VALUES (:post_id, :user_id, :content, NOW())"""
    db.session.execute(
        text(sql), {'post_id': post_id, 'user_id': user_id, 'content': content})
    db.session.commit()
