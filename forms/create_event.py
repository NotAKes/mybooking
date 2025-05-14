import datetime
import os
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, FileField, ValidationError, SelectField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired
from data import db_session
from data.concert_hall import ConcertHall

# форматы изображений и инициализация
ALLOWED_SUFFIXES = ['.png', '.jpg', '.jpeg']
db_session.global_init("db/database.db")


# проверка на картинку
def check_suffix(form, field):
    if not form.image.data.filename:
        return
    if os.path.splitext(form.image.data.filename)[-1] not in ALLOWED_SUFFIXES:
        raise ValidationError('Field must be image')


# проверка даты
def check_outdated(form, field):
    if form.start_date.data < datetime.datetime.now():
        raise ValidationError('This date is unavailable')


# получение концертных залов
def get_halls():
    db_sess = db_session.create_session()
    formatted_list = []
    for i in db_sess.query(ConcertHall).all():
        formatted_list.append((i.id, i.fullname))
    return formatted_list


# класс формы ивента
class CreateEvent(FlaskForm):
    name = StringField('Название мероприятия', validators=[DataRequired()])
    about = TextAreaField("Описание мероприятия")
    place = SelectField('Адрес', validators=[DataRequired()],
                        choices=get_halls())
    price = StringField('Цена билета')
    image = FileField('Изображение', validators=[check_suffix])
    start_date = DateTimeLocalField('Дата начала', validators=[DataRequired(), check_outdated])
    submit = SubmitField('Создать')
