from sqlalchemy.sql import text
from db import db


def get_comments_by_post_id(id):
    sql = """SELECT * FROM comments WHERE post_id == :id"""
    result = db.session.execute(text(sql), {'id': id}).fetchall()
    comments = dict(result._asdict())
    return comments
