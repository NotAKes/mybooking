from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


# форма логина
class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
