from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, FileField, ValidationError, EmailField
from wtforms.validators import DataRequired


# форма редактирования поля о себе
class EditAboutForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    about = TextAreaField("Немного о себе", validators=[DataRequired()])
    about_confirm = SubmitField('Изменить информацию о себе', validators=[DataRequired()])


# форма редактирования пароля
class EditPasswdForm(FlaskForm):
    password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    new_password_again = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    passwd_confirm = SubmitField('Изменить пароль')
