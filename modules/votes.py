from sqlalchemy.sql import text
from flask import session
from db import db


def get_votes_by_post_id(id):
    sql = """SELECT COUNT(*) FROM votes WHERE post_id = :post_id"""
    result = db.session.execute(text(sql), {'post_id': id})
    votes = result.fetchone()[0]
    return votes


def if_voted(post_id, user_id):
    sql = """SELECT COUNT(*) FROM votes WHERE post_id = :post_id AND user_id = :user_id"""
    result = db.session.execute(
        text(sql), {'post_id': post_id, 'user_id': user_id})
    already_voted = result.fetchone()[0]
    return already_voted == 1


def vote_post(post_id):
    user_id = session["user_id"]
    if if_voted(post_id):
        return False
    sql = """INSERT INTO votes (user_id, post_id) VALUES (:user_id, :post_id)"""
    db.session.execute(text(sql), {'user_id': user_id, 'post_id': post_id})
    db.session.commit()
    return True
