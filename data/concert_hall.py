import sqlalchemy
from sqlalchemy import orm, ForeignKey
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


# класс концертного зала связанный с ивентом
class ConcertHall(SqlAlchemyBase, UserMixin):
    __tablename__ = 'halls'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    fullname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    capacity = sqlalchemy.Column(sqlalchemy.Integer)
    event = orm.relationship("Event", back_populates='hall')
