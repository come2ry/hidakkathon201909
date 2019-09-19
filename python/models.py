from datetime import datetime
from __init__ import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class iEvent(db.Model):
    __tablename__ = 'i_event'

    # event_id_seq = db.Sequence('event_id_seq', metadata=Base.metadata, start=5001)
    # event_id = db.Column(db.BigInteger, event_id_seq, server_default=event_id_seq.next_value(), nullable=False, autoincrement=True, primary_key=True)
    event_id = db.Column(db.BigInteger, nullable=False, autoincrement=True, primary_key=True)
    event_name = db.Column(db.String(128), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default='0000-00-00 00:00:00')
    end_date = db.Column(db.DateTime, nullable=False, default='0000-00-00 00:00:00')
    location = db.Column(db.String(128), nullable=True)
    target_user =  db.Column(db.String(128), nullable=True)
    created_user_id = db.Column(db.String(128), nullable=False)
    participant_limit_num = db.Column(db.Integer, nullable=False)
    event_detail = db.Column(db.Text)


class iEventImage(db.Model):
    __tablename__ = 'i_event_image'

    event_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    img_binary = db.Column(db.LargeBinary, nullable=False) # mindiumblob


class iEventTag(db.Model):
    __tablename__ = 'i_event_tag'

    event_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    tag_id = db.Column(db.Integer, nullable=False, primary_key=True)


class iEventTargetUserType(db.Model):
    __tablename__ = 'i_event_target_user_type'

    event_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    target_user_type_id = db.Column(db.Integer, nullable=False, primary_key=True)


class iParticipateEvent(db.Model):
    __tablename__ = 'i_participate_event'

    event_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False, primary_key=True)


class iUser(db.Model):
    __tablename__ = 'i_user'

    user_id = db.Column(db.String(128), nullable=False, primary_key=True)
    user_name = db.Column(db.String(128), nullable=True)
    password = db.Column(db.String(128), nullable=False)
    user_comment = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Integer, nullable=False) # tinyint


class mEventTag(db.Model):
    __tablename__ = 'm_event_tag'

    # tag_id_seq = db.Sequence('tag_id_seq', metadata=Base.metadata, start=1001)
    # tag_id = db.Column(db.BigInteger, tag_id_seq, server_default=tag_id_seq.next_value(), nullable=False, autoincrement=True, primary_key=True)
    tag_id = db.Column(db.BigInteger, nullable=False, autoincrement=True, primary_key=True)
    tag_name = db.Column(db.String(128), nullable=False)


class mTargetUserType(db.Model):
    __tablename__ = 'm_target_user_type'

    # target_user_type_id_seq = db.Sequence('tag_id_seq', metadata=Base.metadata, start=11)
    # target_user_type_id = db.Column(db.Integer, target_user_type_id_seq, server_default=target_user_type_id_seq.next_value(), nullable=False, autoincrement=True, primary_key=True)
    target_user_type_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    target_user_type_name = db.Column(db.String(32), nullable=False)
    color_code = db.Column(db.String(64), nullable=False)
