# from flask import Flask, abort
# app = Flask(__name__)

# @app.route('/<path>')
# def index(path):
#     abort(501)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)

# coding: utf-8
from flask import Flask, abort, request, jsonify
from flask_restful import Resource, Api
from config import Config
from __init__ import app, db
from models import *
import logging
# from sqlalchemy import create_engine

# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

api = Api(app)

# def get_user():
#     try:
#         conn = dbh()
#         with conn.cursor() as c:
#             sql = "SELECT * FROM `users` WHERE `id` = %s limit 1"
#             c.execute(sql, [user_id])
#             user = c.fetchone()
#             if user is None:
#                 http_json_error(requests.codes['not_found'], "user not found")
#     except MySQLdb.Error as err:
#         app.logger.exception(err)
#         http_json_error(requests.codes['internal_server_error'], "db error")
#     return user

# # 接続する
# with engine.connect() as con:

#     # テーブルの作成
#     con.execute("CREATE TABLE USERS(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

#     # Insert文を実行する
#     con.execute("INSERT INTO USERS (id, name, age) VALUES(1, 'Kuro', '33')")
#     con.execute("INSERT INTO USERS (id, name, age) VALUES(2, 'Sato', '27')")

#     # Select文を実行する
#     rows = con.execute("select * from users;")
#     for row in rows:
#         print(row)


class Test(Resource):
    def get(self, id):
        events = db.session.query(mEventTag).filter(mEventTag.tag_id==id).all()
        print(events)
        response = jsonify({'user': str(events)})
        response.status_code = 200
        return response

    # def post(self, id):
    #     # users.append(request.json)
    #     response = jsonify({})
    #     response.status_code = 204
    #     return response

    # def put(self):
    #     # user = request.json
    #     response = jsonify({})
    #     response.status_code = 204
    #     return response

    # def delete(self):
    #     # id = request.args.get('id')
    #     response = jsonify({})
    #     response.status_code = 204
    #     return response


class Event(Resource):
    def get(self, id):
        #====TODO:login処理実装後変更====#
        # if logged_in:
        #   me = {}
        # else:
        #   me = None
        # me = get_login_user()
        me = None
        #====TODO:login処理実装後変更====#

        #================properties===================#
        # i_participate_event by <event_id>:
        #   i_user by <user_id> if i_user.os_admin == True:
        #       { user_id: str, user_name: str, is_admin: bool }
        #================properties===================#
        # event_register = get_admin_user(id)

        # is_author
        # if me is None:
        #     is_author = False
        # else:
        #     if me.id == event_register.user_id:
        #         is_author = True
        #     else:
        #         is_author = False

        #================properties===================#
        # i_participate_event by <event_id>:
        #   i_user by <user_id> if i_user.os_admin == False:
        #       [{ user_id: str, user_name: str, is_admin: bool }]
        #================properties===================#
        # attend_users_list = get_attend_users(id)
        # attend_users_id_set = set([user.user_id for user in attend_users_list])

        # is_attend
        #====ASK: is_author -> is_attend = True???====#
        # if is_author:
        #     is_attend = True
        # else:
        #     if me is None:
        #         is_author = False
        #     else:
        #         if me.id in attend_users_id_set:
        #             is_author = True
        #         else:
        #             is_author = False
        #====ASK: is_author -> is_attend = True???====#

        #================properties===================#
        # i_event by <event_id>:
        #   event_id, event_name, start_date, end_date,
        #   location, target_user, created_user_id,
        #   participant_limit_num, (event_detail -> detail_comment)
        #================properties===================#
        # event = get_event(id)


        #================properties===================#
        # i_event_target_user_type by <event_id>:
        #   [target_user_type]
        #================properties===================#
        # target_user_type = get_target_user_type(id)


        #================properties===================#
        # i_event_tag by <event_id>:
        #   [tag_id]
        #================properties===================#
        # tag_list = get_tag_list_from_event_id(id)


        # res_dic = dict(user_id=None)
        response = jsonify({'user': user.get('name')})
        response.status_code = 200
        return response



api.add_resource(Test, '/event/<id>')
# api.add_resource(Event, '/event/<id>')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)