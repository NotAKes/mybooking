import datetime
import sqlalchemy
from sqlalchemy import orm, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .concert_hall import ConcertHall
from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase, UserMixin):
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

    # company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    # stakeholder_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    # company = relationship("Company", foreign_keys=[company_id])
    # stakeholder = relationship("Company", foreign_keys=[stakeholder_id])
