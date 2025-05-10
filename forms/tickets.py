from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from data import db_session

db_session.global_init("db/database.db")


class NumberOfTickets(FlaskForm):
    number_of_tickets = IntegerField('Выберите количество билетов', validators=[DataRequired()])
    submit = SubmitField('Создать')
