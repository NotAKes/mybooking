import datetime
import os
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, FileField, ValidationError
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired

ALLOWED_SUFFIXES = ['.png', '.jpg', '.jpeg']

def check_suffix(form, field):
    if os.path.splitext(form.image.data.filename)[-1] not in ALLOWED_SUFFIXES:
        raise ValidationError('Field must be image')


def check_outdated(form, field):
    if form.start_date.data < datetime.datetime.now() :
        raise ValidationError('This date is unavailable')

class CreateEvent(FlaskForm):
    name = StringField('Название мероприятия', validators=[DataRequired()])
    about = TextAreaField("Описание мероприятия")
    city = StringField('Город', validators=[DataRequired()])
    place = StringField('Адрес', validators=[DataRequired()])
    image = FileField('Изображение', validators=[check_suffix])
    start_date = DateTimeLocalField('Дата начала', validators=[DataRequired(), check_outdated])
    submit = SubmitField('Создать')