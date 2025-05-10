import datetime
import sqlalchemy
from sqlalchemy import orm, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class ConcertHall(SqlAlchemyBase, UserMixin):
    __tablename__ = 'halls'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    fullname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    capacity = sqlalchemy.Column(sqlalchemy.Integer)
    event = orm.relationship("Event", back_populates='hall')
