from flask import Flask, abort, request, jsonify, abort, make_response, send_file, session
from flask_restful import Resource
from __init__ import db, app
from models import *
from auth import get_user
import base64

class Event(Resource):
    # API04
    def get(self, id):
        # sessionからget
        me = get_user()

        #=============== i_event properties ==================#
        # i_event by <event_id>:
        #   event_id, event_name, start_date, end_date,
        #   location, target_user, created_user_id,
        #   participant_limit_num, (event_detail -> detail_comment)
        #=============== i_event properties ==================#
        event = db.session.query(iEvent).filter_by(event_id=id).one_or_none()

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
                # if registered_user is not None:
                #     # registered_user 複数人!?
                #     abort(404)

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
            # ASK:user is Noneは考えない？
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
            if me.user_id == registered_user.get('user_id'):
                is_author = True
            else:
                is_author = False

        # is_attend
        is_attend = False
        if me is None:
            is_attend = False
        else:
            attend_user_ids_set = set([user.get('user_id') for user in attend_user_list])
            if me.user_id in attend_user_ids_set:
                is_attend = True
            else:
                is_attend = False


        #=============== i_event_target_user_type properties ==================#
        # i_event_target_user_type by <event_id>:
        #   [target_user_type]
        #=============== i_event_target_user_type properties ==================#
        target_user_type_row = db.session.query(iEventTargetUserType).filter_by(event_id=id).order_by(iEventTargetUserType.target_user_type_id.asc()).all()
        target_user_type = [t.target_user_type_id for t in target_user_type_row]


        #=============== i_event_tag properties ==================#
        # i_event_tag by <event_id>:
        #   [tag_id]
        #=============== i_event_tag properties ==================#
        # ASK:昇順じゃなくていいの？
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

    # API05
    # 存在しないtag_listはok?
    def post(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        # json_data = request.get_json(force=True)
        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])

        event_name = json_data.get('event_name')
        start_date = json_data.get('start_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_date = json_data.get('end_date')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        location = json_data.get('location', '')
        target_user_type = json_data.get('target_user_type', '')
        target_user = json_data.get('target_user', '')
        participant_limit_num = int(json_data.get('participant_limit_num'))
        image_binary = json_data.get('image_binary', None)
        detail_comment = json_data.get('detail_comment', '')
        tag_list = json_data.get('tag_list', '')


        if participant_limit_num < 1 or event_name == '' or start_date == '' or end_date == '' or target_user_type == '':
            response = make_response("", 400)
            return response

        _target_user_type_list = db.session.query(mTargetUserType).all()
        target_user_type_list = [int(t.target_user_type_id) for t in _target_user_type_list]

        t_list = list(map(int, target_user_type.split(',')))
        for t in t_list:
            if t not in target_user_type_list:
                response = make_response("", 400)
                return response


        args = dict(
            event_name=event_name,
            start_date=start_date,
            end_date=end_date,
            location=location,
            target_user=target_user,
            created_user_id=me.user_id,
            participant_limit_num=participant_limit_num,
            event_detail=detail_comment,
        )


        event = iEvent(**args)
        db.session.add(event)
        db.session.commit()

        if image_binary is not None:
            # TODO:ここはわからん
            event_image = iEventImage(**dict(event_id=event.event_id, img_binary=image_binary.encode()))
            db.session.add(event_image)


        tag_list = list(map(int, tag_list.split(',')))
        event_tag_list = []
        for tag_id in tag_list:
            event_tag_list += [iEventTag(**dict(event_id=event.event_id, tag_id=tag_id))]

        target_user_type_list_list = []
        for target_type_id in target_user_type_list:
            target_user_type_list_list += [iEventTargetUserType(**dict(event_id=event.event_id, target_user_type_id=target_type_id))]

        db.session.add_all(event_tag_list)
        db.session.add_all(target_user_type_list_list)
        db.session.commit()

        res_dic = dict(event_id=event.event_id)
        response = jsonify(res_dic)
        response.status_code = 200
        return response

    # API06
    def put(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])
        event_name = json_data.get('event_name')
        start_date = json_data.get('start_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_date = json_data.get('end_date')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        location = json_data.get('location', '')
        target_user_type = json_data.get('target_user_type', '') # 更新必須
        target_user = json_data.get('target_user', '')
        participant_limit_num = int(json_data.get('participant_limit_num'))
        image_binary = json_data.get('image_binary', None)
        detail_comment = json_data.get('detail_comment', '')
        tag_list = json_data.get('tag_list', '') # 更新必須
        event_id = int(json_data.get('event_id'))



        if participant_limit_num < 1 or event_name == '' or start_date == '' or end_date == '' or target_user_type == '':
            response = make_response("", 400)
            return response


        _target_user_type_list = db.session.query(mTargetUserType).all()
        target_user_type_list = [int(t.target_user_type_id) for t in _target_user_type_list]

        target_list = list(map(int, target_user_type.split(',')))
        for t in target_list:
            if t not in target_user_type_list:
                response = make_response("", 400)
                return response

        _tag_list = db.session.query(mEventTag).all()
        exists_tag_list = [int(t.tag_id) for t in _tag_list]

        if tag_list == '':
            tag_list = []
        else:
            tag_list = list(map(int, tag_list.split(',')))
        for t in tag_list:
            if t not in exists_tag_list:
                response = make_response("", 400)
                return response


        event = db.session.query(iEvent).filter_by(event_id=event_id).one_or_none()
        # print(event.__dict__)
        if event is None:
            response = make_response("", 400)
            return response
        if event.created_user_id != me.user_id:
            response = make_response("", 403)
            return response

        event.event_name = event_name
        event.start_date = start_date
        event.end_date = end_date
        event.location = location
        event.target_user = target_user
        event.participant_limit_num = participant_limit_num
        if image_binary is not None:
            # TODO:ここはわからん
            event_image = db.session.query(iEventImage).filter_by(event_id=event.event_id).one_or_none()
            event_image.image_binary = base64.b64decode(image_binary)
        event.event_detail = detail_comment

        target_user_type_list = []
        for target_type_id in target_list:
            target_user_type_list += [iEventTargetUserType(event_id=event.event_id, target_user_type_id=target_type_id)]
        event.target_user_type_list = target_user_type_list

        tag_list_list = []
        for tag_id in tag_list:
            tag_list_list += [iEventTag(event_id=event.event_id, tag_id=tag_id)]
        event.tag_list = tag_list_list

        db.session.commit()

        response = make_response("", 200)
        return response

    # API07
    def delete(self, id):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        event = db.session.query(iEvent).filter_by(event_id=id).one_or_none()
        if event is None:
            response = make_response("", 400)
            return response

        if event.created_user_id != me.user_id:
            response = make_response("", 403)
            return response

        db.session.delete(event)
        db.session.commit()

        response = make_response("", 200)
        return response

# API09
class EventCancel(Resource):
    def post(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])
        event_id = json_data.get('event_id')

        event = db.session.query(iEvent).filter_by(event_id=event_id).one_or_none()
        if event is None:
            response = make_response("", 400)
            return response

        attend_user_id_list = [u.user_id for u in event.users_list]
        if me.user_id not in attend_user_id_list:
            response = jsonify({"message":"イベントに参加していません。"})
            response.status_code = 200
            return response

        new_users_list = []
        for u in event.users_list:
            if u.user_id == me.user_id:
                continue
            new_users_list += [u]

        event.users_list = new_users_list
        db.session.commit()
        response = make_response("", 200)
        return response

# API08
class EventAttend(Resource):
    def post(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        form_data = request.form
        if len(request.form) == 0:
            json_data = request.get_json(force=True)
        else:
            json_data = dict([(k, v) for k, v in form_data.items()])
        event_id = json_data.get('event_id')

        event = db.session.query(iEvent).filter_by(event_id=event_id).one_or_none()
        if event is None:
            response = make_response("", 400)
            return response

        attend_user_id_list = [u.user_id for u in event.users_list]
        if me.user_id in attend_user_id_list:
            response = jsonify({"message":"既にイベントに参加しています。"})
            response.status_code = 200
            return response

        if event.participant_limit_num < len(event.users_list)+1:
            response = jsonify({"message":"イベントの定員に達しています。"})
            response.status_code = 200
            return response

        event.users_list += [iParticipateEvent(**dict(
            event_id=event_id,
            user_id=me.user_id
        ))]
        db.session.commit()

        target_user_type = [target.target_user_type_id for target in event.target_user_type_list]
        tag_list = [tag.tag_id for tag in event.tag_list]

        attend_user_list = []
        registered_user = None
        for u in event.users_list:
            user = db.session.query(iUser).filter_by(user_id=u.user_id).one_or_none()
            if user.user_id == event.created_user_id:
                registered_user = dict(
                    user_id=user.user_id,
                    user_name=user.user_name,
                    is_admin=True if user.is_admin else False
                )
            attend_user_list += [dict(
                user_id=u.user_id,
                user_name=user.user_name,
                is_admin=True if user.is_admin else False
            )]

        if registered_user is None:
            _user = db.session.query(iUser).filter_by(user_id=event.created_user_id).one_or_none()
            registered_user = dict(
                user_id=_user.user_id,
                user_name=_user.user_name,
                is_admin=True if _user.is_admin else False
            )


        is_author = True if event.created_user_id == me.user_id else False

        res_dic = dict(
            event_id=event_id,
            event_name=event.event_name,
            start_date=event.get_start_date(),
            end_date=event.get_end_date(),
            location=event.location,
            target_user_type=target_user_type,
            target_user=event.target_user,
            registered_user=registered_user,
            detail_comment=event.event_detail,
            tag_list=tag_list,
            attend_user_list=attend_user_list,
            is_author=is_author,
            participant_limit_num=event.participant_limit_num
        )

        response = jsonify(res_dic)
        response.status_code = 200
        return response


class EventRecommend(Resource):
    def get(self):
        # sessionからget
        me = get_user()
        if me is None:
            response = make_response("", 401)
            return response

        app.logger.debug(me)

        my_tag_value_dict = {}
        _particaipate_event = db.session.query(iParticipateEvent).filter_by(user_id=me.user_id).all()

        past_events = []
        _past_events = []
        future_events = {}
        for p_event in _particaipate_event:
            e = p_event.event
            now = datetime.now()
            _tag_list = [(t.tag_id, t.event_id) for t in e.tag_list]
            tag_list = [(t.tag_id, t.event_id) for t in e.tag_list]
            if e.end_date < now:
                past_events += [tag_list]
                _past_events += [_tag_list]
            else:
                # TODO: 参加中は評価に含めるか
                if e.start_date < now:
                    continue
                future_events[e.event_id] = tag_list

        app.logger.debug('489', future_events, _past_events)
        # return make_response("", 200)

        for p_tag in past_events:
            for t in p_tag:
                if my_tag_value_dict.get(t, None) is None:
                    my_tag_value_dict[t] = 1/len(p_tag)
                else:
                    my_tag_value_dict[t] += 1/len(p_tag)

        _event_info_list = []
        for f_e_id, f_tag_list in future_events.items():
            if len(f_tag_list) == 0:
                continue
            sum_ = 0
            for f_t in f_tag_list:
                v = my_tag_value_dict.get(f_t, 0)
                sum_ += v

            score = sum_/len(f_tag_list)
            _event_info_list += [(f_e_id, score)]

        _event_info_list.sort(key=lambda x: -x[1]*1000000+x[1])
        app.logger.debug('511', _event_info_list)

        if _event_info_list is None:
            app.logger.debug('513', _event_info_list)
            _event_info_list = []

        _target_user_type_list = db.session.query(mTargetUserType).order_by(mTargetUserType.target_user_type_id.asc()).all()
        color_code_dict = dict([(t.target_user_type_id, t.color_code) for t in _target_user_type_list])

        event_info_list = []
        for e_id, score in _event_info_list:
            if score == 0:
                continue

            event = db.session.query(iEvent).filter_by(event_id=e_id).one_or_none()

            color_code = "#999900"
            if len(e.target_user_type_list) <= 1:
                color_code = color_code_dict[e.target_user_type_list[0].target_user_type_id]

            event_info_list += [dict(
                event_id=e_id,
                event_name=event.event_name,
                start_date=event.get_start_date(),
                end_date=event.get_end_date(),
                color_code=color_code
            )]

        event_info_list = event_info_list[:10]
        app.logger.debug('event_info_list', event_info_list)
        response = jsonify(dict(event_info_list=event_info_list))
        response.status_code = 200
        return response