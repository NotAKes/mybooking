import os
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, FileField, ValidationError
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired

ALLOWED_SUFFIXES = ['.png', '.jpg']

def check_suffix(form, field):
    print(os.path.splitext(form.image.data)[-1])
    if os.path.splitext(form.image.data)[-1] not in ALLOWED_SUFFIXES:
        raise ValidationError('Field must be image')


class CreateEvent(FlaskForm):
    name = StringField('Название мероприятия', validators=[DataRequired()])
    about = TextAreaField("Описание мероприятия")
    city = StringField('Город', validators=[DataRequired()])
    place = StringField('Адрес', validators=[DataRequired()])
    image = FileField('Изображение', validators=[DataRequired()])
    start_date = DateTimeLocalField('Дата начала', validators=[DataRequired()])
    submit = SubmitField('Создать')