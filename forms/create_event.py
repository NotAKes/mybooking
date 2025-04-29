from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.datetime import DateTimeLocalField

from wtforms.validators import DataRequired


class CreateEvent(FlaskForm):
    name = StringField('Название мероприятия', validators=[DataRequired()])
    about = TextAreaField("Описание мероприятия")
    city = StringField('Город', validators=[DataRequired()])
    place = StringField('Адрес', validators=[DataRequired()])
    start_date = DateTimeLocalField('Дата начала')
    submit = SubmitField('Создать')