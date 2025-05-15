import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


# класс ивента связанный с концертным залом
class Event(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'events'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    path_to_file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    start_date_formatted = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    capacity_left = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    place = sqlalchemy.Column(sqlalchemy.String)
    hall_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("halls.id"))
    hall = orm.relationship('ConcertHall')
