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
from __init__ import app
from sqlalchemy import create_engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

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


class User(Resource):
    def get(self):
        id = request.args.get('id')
        user = {'name': 'guest'}
        # user = get_user(id)
        response = jsonify({'user': user.get('name')})
        response.status_code = 200
        return response

    def post(self):
        # users.append(request.json)
        response = jsonify({})
        response.status_code = 204
        return response

    def put(self):
        # user = request.json
        response = jsonify({})
        response.status_code = 204
        return response

    def delete(self):
        # id = request.args.get('id')
        response = jsonify({})
        response.status_code = 204
        return response

api.add_resource(User, '/user')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)