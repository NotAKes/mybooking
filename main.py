from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required
from data.event import Event
from forms.user import RegisterForm
from forms.create_event import CreateEvent
from data.users import User
from data import db_session
from forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.run()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    events = sorted(db_sess.query(Event).all(), key=lambda a: a.start_date)

    return render_template("index.html", events=events)


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route('/event/create', methods=['GET', 'POST'])
def create_event():
    form = CreateEvent()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        start_date_formatted = form.start_date.data.strftime("%d %B %H:%M")
        event = Event(
            name=form.name.data,
            about=form.about.data,
            city=form.city.data,
            place=form.place.data,
            start_date=form.start_date.data,
            start_date_formatted=start_date_formatted
        )
        db_sess.add(event)
        db_sess.commit()
        return redirect('/')
    return render_template('create_event.html', title='Создание мероприятия', form=form)


if __name__ == '__main__':
    main()
