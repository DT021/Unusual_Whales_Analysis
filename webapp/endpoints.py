from flask import jsonify

from webapp.app import db


def get_players_from_db():
    sql = """select * from playerinfo limit 10"""
    return jsonify(db.query_db(sql))

