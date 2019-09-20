from flask import Flask, abort, request, jsonify, abort, make_response, send_file, session
from flask_restful import Resource
from __init__ import db
from models import *
from auth import get_user

class Admin(Resource):
    # API015
    def get(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        users = db.session.query(iUser).all()
        user_list = []
        for user in users:
            user_list += [dict(
                user_id=user.user_id,
                user_name=user.user_name,
                user_comment=user.user_comment,
                is_admin=True if user.is_admin else False
            )]

        response = jsonify(dict(
            user_list=user_list
        ))
        response.status_code = 200
        return response

    # API016
    def post(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])
        user_id = json_data.get('user_id')
        user_name = json_data.get('user_name', '')
        user_comment = json_data.get('user_comment', '')
        password = json_data.get('password', '')
        is_admin = json_data.get('is_admin', 0)

        user = iUser(**dict(
            user_id=user_id,
            user_name=user_name,
            user_comment=user_comment,
            password=password,
            is_admin=True if is_admin else False
        ))

        db.session.add(user)
        db.session.commit()

        response = make_response("", 200)
        return response

    # API017
    def put(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])
        user_id = json_data.get('user_id')
        user_name = json_data.get('user_name', '')
        user_comment = json_data.get('user_comment', '')
        password = json_data.get('password', None)
        is_admin = json_data.get('is_admin', 0)

        user = db.session.query(iUser).filter_by(user_id=user_id).one_or_none()
        if user is None:
            response = make_response("", 400)
            return response

        user.user_id = user_id
        user.user_name = user_name
        user.user_comment = user_comment
        if password is not None:
            user.password = password
        user.is_admin = 1 if is_admin else 0

        db.session.commit()

        response = make_response("", 200)
        return response

    # API018
    def delete(self, id):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        user = db.session.query(iUser).filter_by(user_id=id).one_or_none()
        if user is None:
            response = make_response("", 400)
            return response

        db.session.delete(user)
        db.session.commit()

        response = make_response("", 200)
        return response


class AdminTag(Resource):
    # API19
    def get(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        _tag_list = db.session.query(mEventTag).order_by(mEventTag.tag_id.asc()).all()
        tag_list = []
        for t in _tag_list:
            tag_list += [dict(
                tag_id=t.tag_id,
                tag_name=t.tag_name
            )]

        response = jsonify(dict(tag_list=tag_list))
        response.status_code = 200
        return response

    # API20
    def post(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])
        tag_name = json_data.get('tag_name')

        tag = db.session.query(mEventTag).filter_by(tag_name=tag_name).one_or_none()
        if tag is not None:
            response = make_response("", 400)
            return response

        tag = mEventTag(tag_name=tag_name)
        db.session.add(tag)
        db.session.commit()

        response = make_response("", 200)
        return response

    # API21
    def delete(self, id):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        tag = db.session.query(mEventTag).filter_by(tag_id=id).one_or_none()
        if tag is None:
            response = make_response("", 400)
            return response

        db.session.delete(tag)
        db.session.commit()

        response = make_response("", 200)
        return response


class AdminTargetType(Resource):
    # API22
    def get(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        # tag = db.session.query(mEventTag).filter_by(tag_id=id).one_or_none()
        _target_user_type_list = db.session.query(mTargetUserType).order_by(mTargetUserType.target_user_type_id.asc()).all()
        target_user_type_list = []
        for t in _target_user_type_list:
            target_user_type_list += [dict(
                target_user_type_id=t.target_user_type_id,
                target_user_type_name=t.target_user_type_name,
                color_code=t.color_code
            )]

        response = jsonify(dict(target_user_type_list=target_user_type_list))
        response.status_code = 200
        return response

    # API23
    def post(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])
        target_user_type_name = json_data.get('target_user_type_name')
        color_code = json_data.get('color_code')

        target = db.session.query(mTargetUserType).filter_by(target_user_type_name=target_user_type_name).one_or_none()
        if target is not None:
            response = make_response("", 400)
            return response

        target = mTargetUserType(**dict(
            target_user_type_name=target_user_type_name,
            color_code=color_code
        ))

        db.session.add(target)
        db.session.commit()

        response = make_response("", 200)
        return response

    # API24
    def put(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])
        target_user_type_id = json_data.get('target_user_type_id')
        target_user_type_name = json_data.get('target_user_type_name')
        color_code = json_data.get('color_code')

        target = db.session.query(mTargetUserType).filter_by(target_user_type_id=target_user_type_id).one_or_none()
        if target is None:
            response = make_response("", 400)
            return response

        target.target_user_type_name = target_user_type_name
        target.color_code = color_code

        db.session.commit()

        response = make_response("", 200)
        return response

    # API25
    def delete(self, id):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        if not me.is_admin:
            response = make_response("", 403)
            return response

        target = db.session.query(mTargetUserType).filter_by(target_user_type_id=id).one_or_none()
        if target is None:
            response = make_response("", 400)
            return response

        db.session.delete(target)
        db.session.commit()

        response = make_response("", 200)
        return response