import os
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.event import Event
from forms.user import RegisterForm
from forms.create_event import CreateEvent
from sqlalchemy import func
from data.users import User
from data import db_session
from forms.login import LoginForm
from werkzeug.utils import secure_filename
import flask
from forms.profile import EditAboutForm, EditPasswdForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

user_blueprint = flask.Blueprint(
    'user_blueprint',
    __name__,
    template_folder='templates'
)

api_blueprint = flask.Blueprint(
    'api_blueprint',
    __name__,
    template_folder='templates'
)


def main():
    db_session.global_init("db/database.db")
    app.register_blueprint(user_blueprint)
    app.register_error_handler(401, err401)
    app.register_error_handler(404, err404)
    app.run()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@user_blueprint.route("/")
def index():
    db_sess = db_session.create_session()

    events = sorted(db_sess.query(Event).all(), key=lambda a: a.start_date)

    return render_template("index.html", events=events)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@user_blueprint.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    got_id = current_user.get_id()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == got_id).first()
    if not user.is_admin:
        return redirect('/')
    form = CreateEvent()
    if form.validate_on_submit():
        start_date_formatted = form.start_date.data.strftime("%d %B %Y %H:%M ")
        id_counter = db_sess.query(func.count(Event.id)).scalar() + 1
        filename = secure_filename(str(id_counter) + os.path.splitext(form.image.data.filename)[-1])
        form.image.data.save('static/images/' + filename)
        event = Event(
            name=form.name.data,
            about=form.about.data,
            city=form.city.data,
            place=form.place.data,
            path_to_file=filename,
            start_date=form.start_date.data,
            start_date_formatted=start_date_formatted
        )
        db_sess.add(event)
        db_sess.commit()

        return redirect('/')
    return render_template('create_event.html', title='Создание мероприятия', form=form)


@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    got_id = current_user.get_id()
    form_about = EditAboutForm(name=current_user.name, about=current_user.about, email=current_user.email)
    form_passwd = EditPasswdForm()
    db_sess = db_session.create_session()
    if form_about.validate_on_submit() and form_about.about_confirm.data:
        user = db_sess.query(User).filter(User.id == got_id).first()
        user.email = form_about.email.data
        user.name = form_about.name.data
        user.about = form_about.about.data
        db_sess.commit()
        return redirect('/')
    if form_passwd.validate_on_submit() and form_passwd.passwd_confirm.data:
        user = db_sess.query(User).filter(User.id == got_id).first()
        user.set_password(form_passwd.new_password.data)
        db_sess.commit()
        return redirect('/')
    return render_template('profile.html', title='Ваш профиль', form_about=form_about, form_passwd=form_passwd)
    # TODO


@user_blueprint.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile_view(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    list_of_favorites = ['Здесь', 'будет', 'список', 'любимых']
    user_form = {
        'username': user.name,
        'about': user.about,
        'favorite_events': list_of_favorites,
        'num_of_favorite':len(list_of_favorites)
    }
    return render_template('profile_view.html', user_form=user_form)


@user_blueprint.route('/event/<int:id>', methods=['GET', 'POST'])
@login_required
def get_event_id(id):
    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.id == id).first()
    fields = {
        'name': event.name,
        'about': event.about,
        'place': event.place,
        'city': event.city,
        'path': event.path_to_file,
        'date': event.start_date_formatted

    }

    return render_template('id_event.html', title=event.name, form=fields)


@user_blueprint.errorhandler(401)
def err401(e):
    return redirect('/login')


@user_blueprint.errorhandler(404)
def err404(e):
    return render_template('error404.html')


@user_blueprint.route('/development')
def development():
    return render_template('development.html')


if __name__ == '__main__':
    main()
