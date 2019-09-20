# coding: utf-8
from flask import Flask, abort, request, jsonify, abort, make_response, send_file
from flask_restful import Resource, Api
from pprint import pprint
from config import Config
from __init__ import app, db
from models import *
from auth import *
from event import *
from admin import *
from sqlalchemy import func
import logging
import io
import calendar
# from sqlalchemy import create_engine

# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

api = Api(app)
# TODO: 昇順 order_by確認


# class Test(Resource):
#     def get(self, id):
#         events = db.session.query(mEventTag).filter(mEventTag.tag_id==id).all()
#         # pprint(events)
#         response = jsonify({'user': str(events)})
#         response.status_code = 200
#         return response

class Top(Resource):
    # API03
    def get(self):
        # sessionからget
        me = get_user()

        # ImmutableMultiDict([('target_year', '2019'), ('target_month', '9')])
        now = datetime.now()
        target_year = request.args.get('target_year', now.year)
        target_month = request.args.get('target_month', now.month)
        # print(target_year, target_month)

        # _, lastday = calendar.monthrange(a.year,a.month)
        events = db.session.query(iEvent).filter(func.extract('year', iEvent.start_date) == target_year, func.extract('month', iEvent.start_date) == target_month).all()
        # print(events)

        tag_list = db.session.query(mEventTag).order_by(mEventTag.tag_id.asc()).all()
        tag_list = [dict(tag_id=t.tag_id, tag_name=t.tag_name) for t in tag_list]

        _target_user_type_list = db.session.query(mTargetUserType).order_by(mTargetUserType.target_user_type_id.asc()).all()
        target_user_type_list = [dict(target_user_type_id=t.target_user_type_id, target_user_type_name=t.target_user_type_name, color_code=t.color_code) for t in _target_user_type_list]

        color_code_dict = dict([(t.target_user_type_id, t.color_code) for t in _target_user_type_list])

        event_info_list = []
        for e in events:
            color_code = "#999900"
            if len(e.target_user_type_list) <= 1:
                color_code = color_code_dict[e.target_user_type_list[0].target_user_type_id]

            # print(e.target_user_type_list, color_code)

            event_info_list += [dict(
                event_id=e.event_id,
                event_name=e.event_name,
                start_date=e.get_start_date(),
                end_date=e.get_end_date(),
                color_code=color_code
            )]


        res_dic = dict(
            event_info_list=event_info_list,
            tag_list=tag_list,
            target_user_type_list=target_user_type_list
        )

        if me is not None:
            res_dic['user_id'] = me.user_id
            res_dic['user_name'] = me.user_name
            res_dic['is_admin'] = me.is_admin

        response = jsonify(res_dic)
        response.status_code = 200
        return response

class User(Resource):
    # API12
    def get(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        user = db.session.query(iUser).filter_by(user_id=me.user_id).one_or_none()
        events = db.session.query(iParticipateEvent).filter_by(user_id=me.user_id).order_by(iParticipateEvent.event_id.asc()).all()
        _target_user_type_list = db.session.query(mTargetUserType).all()
        color_code_dict = dict([(t.target_user_type_id, t.color_code) for t in _target_user_type_list])

        event_info_list = []
        for _e in events:
            e = _e.event
            color_code = "#999900"
            target_list = e.target_user_type_list
            if len(target_list) <= 1:
                color_code = color_code_dict[target_list[0].target_user_type_id]

            # print(e.event.target_user_type_list, color_code)

            event_info_list += [dict(
                event_id=e.event_id,
                event_name=e.event_name,
                start_date=e.get_start_date(),
                end_date=e.get_end_date(),
                color_code=color_code
            )]

        res_dic = dict(
            user_name=me.user_name,
            user_comment=user.user_comment,
            event_info_list=event_info_list
        )
        response = jsonify(res_dic)
        response.status_code = 200
        return response

    # API14
    def put(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        form_data = request.form
        json_data = dict([(k, v) for k, v in form_data.items()])
        user_name = json_data.get('user_name', '')
        user_comment = json_data.get('user_comment', '')

        user = db.session.query(iUser).filter_by(user_id=me.user_id).one_or_none()
        user.user_name = user_name
        user.user_comment = user_comment
        db.session.commit()

        response = make_response("", 200)
        return response



class Other(Resource):
    # API13
    def get(self, id):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        user = db.session.query(iUser).filter_by(user_id=id).one_or_none()
        events = db.session.query(iParticipateEvent).filter_by(user_id=id).order_by(iParticipateEvent.event_id.asc()).all()
        _target_user_type_list = db.session.query(mTargetUserType).all()
        color_code_dict = dict([(t.target_user_type_id, t.color_code) for t in _target_user_type_list])

        event_info_list = []
        for _e in events:
            e = _e.event
            color_code = "#999900"
            target_list = e.target_user_type_list
            if len(target_list) <= 1:
                color_code = color_code_dict[target_list[0].target_user_type_id]

            # print(e.event.target_user_type_list, color_code)

            event_info_list += [dict(
                event_id=e.event_id,
                event_name=e.event_name,
                start_date=e.get_start_date(),
                end_date=e.get_end_date(),
                color_code=color_code
            )]

        res_dic = dict(
            user_name=user.user_name,
            user_comment=user.user_comment,
            event_info_list=event_info_list
        )
        response = jsonify(res_dic)
        response.status_code = 200
        return response

# API10
class Image(Resource):
    def get(self, id):
        image = db.session.query(iEventImage).filter_by(event_id=id).one_or_none()
        if image is None:
            response = make_response("", 404)
            return response

        image_bin = image.img_binary
        return send_file(
            io.BytesIO(image_bin),
            mimetype='image/png'
        )


# api.add_resource(Test, '/event/<id>')
api.add_resource(Event, '/event/<id>', '/event')
api.add_resource(EventCancel, '/event/cancel')
api.add_resource(EventAttend, '/event/attend')
api.add_resource(Image, '/event/image/<id>')
api.add_resource(Top, '/top')
api.add_resource(User, '/user')
api.add_resource(Other, '/user/<id>')
api.add_resource(Admin, '/admin/user/<id>', '/admin/users', '/admin/user')
api.add_resource(AdminTag, '/admin/tag/<id>', '/admin/tag')
api.add_resource(AdminTargetType, '/admin/target_user_type/<id>', '/admin/target_user_type')
api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)