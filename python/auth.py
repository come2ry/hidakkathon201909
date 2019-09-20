from flask import Flask, abort, request, jsonify, abort, make_response, send_file, session
from flask_restful import Resource
from __init__ import db
from models import *


# class iUser(db.Model):
#     __tablename__ = 'i_user'

#     user_id = db.Column(db.String(128), nullable=False, primary_key=True)
#     user_name = db.Column(db.String(128), nullable=True)
#     password = db.Column(db.String(128), nullable=False)
#     user_comment = db.Column(db.Text, nullable=False)
#     is_admin = db.Column(db.Integer, nullable=False) # tinyint


def set_session(user_id: str, user_name: str, is_admin: bool) -> None:
    session['user_id'] = user_id
    session['user_name'] = user_name
    session['is_admin'] = is_admin # bool
    session['is_loggedin'] = True

def clear_session():
    session.clear()


def get_user():
    if 'is_loggedin' in session:
        me = iUser(**dict(user_id=session['user_id'], user_name=session['user_name'], is_admin=session['is_admin']))
    else:
        me = None

    return me


class Login(Resource):
    def post(self):
        form_data = request.form
        json_data = dict([(k, v) for k, v in form_data.items()])
        user_id = json_data.get('user_id')
        password = json_data.get('password')

        user = db.session.query(iUser).filter_by(user_id=user_id).one_or_none()
        if user is None or user.password != password:
            response = make_response("", 401)
            return response

        set_session(user.user_id, user.user_name, True if user.is_admin else False)

        res_dic = dict(
            user_id=user.user_id,
            user_name=user.user_name,
            is_admin=True if user.is_admin else False
        )

        # users.append(request.json)
        response = jsonify(res_dic)
        response.status_code = 200
        return response


class Logout(Resource):
    def post(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response
        # if not session.get('is_loggedin', False):
        #     print(64, session.get('is_loggedin', False))
        #     print(session.__dict__)
        #     response = make_response("", 401)
        #     return response

        clear_session()
        response = make_response("", 200)
        return response