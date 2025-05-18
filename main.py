import os

from aiogram.utils.chat_member import USERS
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.concert_hall import ConcertHall
from data.event import Event
from forms.user import RegisterForm
from forms.create_event import CreateEvent
from forms.tickets import NumberOfTickets
from sqlalchemy import func
from data.users import User
from data import db_session
from forms.login import LoginForm
from werkzeug.utils import secure_filename
import flask
from data.events_api import EventListResource, EventResource
from flask_restful import Api
from wtforms import ValidationError
from forms.profile import EditAboutForm, EditPasswdForm
import logging

# создание приложения
app = Flask(__name__)

# конфиг и папки
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

# подключение апи
api = Api(app)
api.add_resource(EventListResource, '/api/events')
api.add_resource(EventResource, '/api/events/<events_id>')

# логгирование
logging.basicConfig(
    filename='logs.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

# схема для основных ссылок
user_blueprint = flask.Blueprint(
    'user_blueprint',
    __name__,
    template_folder='templates'
)


# создание и инициализация
def main():
    db_session.global_init("db/database.db")
    app.register_blueprint(user_blueprint)
    app.register_error_handler(401, err401)
    app.register_error_handler(404, err404)
    app.run(host='0.0.0.0', port=80)


# логин
login_manager = LoginManager()
login_manager.init_app(app)


# загрузка пользователей
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# главная
@user_blueprint.route("/")
def index():
    db_sess = db_session.create_session()
    # вывод ивентов
    events = sorted(db_sess.query(Event).all(), key=lambda a: a.start_date)
    return render_template("index.html", events=events)


# страница регистрации
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # ошибки
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        id_counter = db_sess.query(func.count(User.id)).scalar() + 1
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        # создание пользователя
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        logging.warning(f'Account {user} created. Id {id_counter}')
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# страница логина
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        # корректный логин
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            logging.warning(f'Account {user.name} logged. Id {user.id}')
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# выход
@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# созданте ивента
@user_blueprint.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    got_id = current_user.get_id()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == got_id).first()
    halls = db_sess.query(ConcertHall).all()
    # если не админ то редирект на главную
    if not user.is_admin:
        return redirect('/')
    form = CreateEvent()
    # заполнение полей
    if form.validate_on_submit():
        start_date_formatted = form.start_date.data.strftime("%d %B %Y %H:%M ")
        # вычисление последнего ид ивента для сохранения картинки с этим ид
        id_counter = db_sess.query(func.count(Event.id)).scalar() + 1
        filename = secure_filename(str(id_counter) + os.path.splitext(form.image.data.filename)[-1])
        form.image.data.save('static/images/' + filename)
        hall = db_sess.query(ConcertHall).filter(ConcertHall.id == int(form.place.data)).first()
        event = Event(
            name=form.name.data,
            about=form.about.data,
            place=hall.fullname,
            path_to_file=filename,
            price=int(form.price.data),
            start_date=form.start_date.data,
            start_date_formatted=start_date_formatted,
            capacity_left=hall.capacity,
            hall_id=hall.id,
            city=hall.city
        )
        db_sess.add(event)
        db_sess.commit()
        logging.warning(f'Account {user.name} created event {event.name}, event Id {id_counter}. User id {user.id}')
        return redirect('/')
    return render_template('create_event.html', title='Создание мероприятия', form=form, halls=halls)


# просмотр своего профиля
@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    got_id = current_user.get_id()
    form_about = EditAboutForm(name=current_user.name, about=current_user.about, email=current_user.email)
    form_passwd = EditPasswdForm()
    db_sess = db_session.create_session()
    # изменение информации о себе
    if form_about.validate_on_submit() and form_about.about_confirm.data:
        user = db_sess.query(User).filter(User.id == got_id).first()
        user.email = form_about.email.data
        user.name = form_about.name.data
        user.about = form_about.about.data
        db_sess.commit()
        return redirect('/')
    # изменение пароля
    if form_passwd.validate_on_submit() and form_passwd.passwd_confirm.data:
        user = db_sess.query(User).filter(User.id == got_id).first()
        user.set_password(form_passwd.new_password.data)
        db_sess.commit()
        return redirect('/')
    return render_template('profile.html', title='Ваш профиль', form_about=form_about, form_passwd=form_passwd)


# просмотр профиля другого человека по ид
@user_blueprint.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile_view(id):
    db_sess = db_session.create_session()
    aviable_ids = [i.id for i in db_sess.query(User).all()]
    if id not in aviable_ids:
        return redirect('/404')
    user = db_sess.query(User).filter(User.id == id).first()
    # задел под добавление любимых событий
    list_of_favorites = ['Здесь', 'будет', 'список', 'любимых']
    user_form = {
        'username': user.name,
        'about': user.about,
        'favorite_events': list_of_favorites,
        'num_of_favorite': len(list_of_favorites)
    }
    return render_template('profile_view.html', user_form=user_form)


# просмотр ивента по ид
@user_blueprint.route('/event/<int:id>', methods=['GET', 'POST'])
@login_required
def get_event_id(id):
    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.id == id).first()
    # информация из полей в словарь
    fields = {
        'id': id,
        'name': event.name,
        'about': event.about,
        'place': event.place,
        'city': event.city,
        'path': event.path_to_file,
        'date': event.start_date_formatted,
        'capacity_left': event.capacity_left
    }

    return render_template('id_event.html', title=event.name, form=fields)


# покупка билетов по ид
@user_blueprint.route('/event/buy/<int:id>', methods=['GET', 'POST'])
@login_required
def buy_ticket(id):
    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.id == id).first()
    form = NumberOfTickets()
    if form.validate_on_submit():
        # проверка на количество билетов
        if form.number_of_tickets.data > event.capacity_left or form.number_of_tickets.data > 7:
            return render_template('buy_ticket.html', event=event, form=form, error='error')
        else:
            # успешная покупка
            event.capacity_left = int(event.capacity_left) - int(form.number_of_tickets.data)
            db_sess.commit()
            return redirect('/event/buy/success')

    return render_template('buy_ticket.html', event=event, form=form)


# страница успешной покупки
@user_blueprint.route('/event/buy/success', methods=['GET', 'POST'])
@login_required
def buy_success():
    return render_template('buy_success.html')


# страница ошибки 401
@user_blueprint.errorhandler(401)
def err401(e):
    return redirect('/login')


# страница ошибки 404
@user_blueprint.errorhandler(404)
def err404(e):
    return render_template('error404.html')


# страница в разработке
@user_blueprint.route('/development')
def development():
    return render_template('development.html')


# запуск
if __name__ == '__main__':
    main()
