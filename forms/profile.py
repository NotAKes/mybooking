from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, FileField, ValidationError, EmailField
from wtforms.validators import DataRequired


class EditAboutForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    about = TextAreaField("Немного о себе", validators=[DataRequired()])
    about_confirm = SubmitField('Изменить информацию о себе', validators=[DataRequired()])


class EditPasswdForm(FlaskForm):
    password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    new_password_again = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    passwd_confirm = SubmitField('Изменить пароль')
