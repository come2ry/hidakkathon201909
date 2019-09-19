# from flask import Flask, abort
# app = Flask(__name__)

# @app.route('/<path>')
# def index(path):
#     abort(501)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)

# coding: utf-8
from flask import Flask, abort, request, jsonify, abort, make_response
from flask_restful import Resource, Api
from config import Config
from __init__ import app, db
from models import *
import logging
# from sqlalchemy import create_engine

# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

api = Api(app)


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
        res_dict = dict()
        #====TODO:login処理実装後変更====#
        # if logged_in:
        #   me = {}
        # else:
        #   me = None
        # me = get_login_user()
        me = None
        #====TODO:login処理実装後変更====#


        #=============== i_event properties ==================#
        # i_event by <event_id>:
        #   event_id, event_name, start_date, end_date,
        #   location, target_user, created_user_id,
        #   participant_limit_num, (event_detail -> detail_comment)
        #=============== i_event properties ==================#
        # event = get_event(id)
        event = db.session.query(iEvent).filter_by(event_id=id).one_or_none()
        # print(event.__dict__)

        # event_id なし
        if event is None:
            response = make_response("", 400)
            return response


        #=============== i_participate_event properties ==================#
        # i_participate_event by <event_id>:
        #   i_user by <user_id> if i_user.os_admin == True:
        #       { user_id: str, user_name: str, is_admin: bool }
        # &
        # i_participate_event by <event_id>:
        #   i_user by <user_id> if i_user.os_admin == False:
        #       [{ user_id: str, user_name: str, is_admin: bool }]
        #=============== i_participate_event properties ==================#

        # fields = [
        #     'id',
        #     'twitter_id']
        # res = cls.query.options(
        #     load_only(*fields)).filter_by(**{key: string}).one_or_none()

        # TODO: N+1なのであとで直す
        registered_user = None
        attend_user_list = []
        events_list = db.session.query(iParticipateEvent).filter_by(event_id=id).all()
        for e in events_list:
            user = db.session.query(iUser).filter_by(user_id=e.user_id).one_or_none()
            if event.created_user_id == user.user_id:
                if registered_user is not None:
                    # registered_user 複数人!?
                    abort(404)

                registered_user = dict(
                    user_id=user.user_id,
                    user_name=user.user_name,
                    is_admin=True if user.is_admin else False
                )

            attend_user_list += [dict(
                user_id=user.user_id,
                user_name=user.user_name,
                is_admin=True if user.is_admin else False
            )]
        if registered_user is None:
            user = db.session.query(iUser).filter_by(user_id=event.created_user_id).first()
            registered_user = dict(
                user_id=user.user_id,
                user_name=user.user_name,
                is_admin=True if user.is_admin else False
            )

        # is_author
        is_author = False
        if me is None:
            is_author = False
        else:
            if me.id == registered_user.get('user_id'):
                is_author = True
            else:
                is_author = False

        # is_attend
        is_attend = False
        if is_author:
            is_attend = True
        else:
            if me is None:
                is_author = False
            else:
                attend_user_ids_set = set([user.get('user_id') for user in attend_user_list])
                if me.id in attend_user_ids_set:
                    is_author = True
                else:
                    is_author = False


        #=============== i_event_target_user_type properties ==================#
        # i_event_target_user_type by <event_id>:
        #   [target_user_type]
        #=============== i_event_target_user_type properties ==================#
        target_user_type_row = db.session.query(iEventTargetUserType).filter_by(event_id=id).all()
        target_user_type = [t.target_user_type_id for t in target_user_type_row]


        #=============== i_event_tag properties ==================#
        # i_event_tag by <event_id>:
        #   [tag_id]
        #=============== i_event_tag properties ==================#
        # tag_list = get_tag_list_from_event_id(id)
        tag_row = db.session.query(iEventTag).filter_by(event_id=id).all()
        tag_list = [t.tag_id for t in tag_row]


        res_dic = dict(
            event_id=event.event_id,
            event_name=event.event_name,
            start_date=event.get_start_date(),
            end_date=event.get_end_date(),
            location=event.location,
            target_user_type=target_user_type,
            target_user=event.target_user,
            registered_user=registered_user,
            participant_limit_num=event.participant_limit_num,
            detail_comment=event.event_detail,
            tag_list=tag_list,
            attend_user_list=attend_user_list,
            is_author=is_author,
            is_attend=is_attend
        )

        response = jsonify(res_dic)
        response.status_code = 200
        return response


class Image(Resource):
    def get(self, event_id):
        return '', 200


# api.add_resource(Test, '/event/<id>')
api.add_resource(Event, '/event/<id>')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)