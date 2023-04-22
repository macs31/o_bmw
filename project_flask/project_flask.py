from flask import Flask, render_template, redirect
from forms.user_forms import RegisterForm, LoginForm
from data import db_session
from data.users import User
from forms.user_forms import RegisterForm, LoginForm
from sqlalchemy import create_engine
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/registration', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', form=form)


@app.route("/details/<int:id>", methods=['GET', 'POST'])
def details(id):
    if not current_user.is_authenticated:
        return redirect('/registration')
    form = DetailsForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if user is None:
        return abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        usr = db_sess.query(User).get(current_user.id)
        usr.age = form.age.data
        usr.weight = form.weight.data
        usr.height = form.height.data
        usr.gender = form.gender.data
        usr.entered_details = True
        db_sess.add(usr)
        db_sess.commit()
        return redirect('/')
    return render_template('details.html', form=form, title='Изменение информации')


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


@app.route('/')
def start():  # Стартовая страница
    return render_template('start.html')


@app.route('/cars')
def cars():
    return render_template('cars.html')


@app.route('/registration')
def registration():  # Регистрация
    return render_template('registration.html')


@app.route('/BMW_X7')
def bmw_x7():  # Регистрация
    return render_template('bmw_x7.html')


@app.route('/BMW_X6')
def bmw_x6():  # Регистрация
    return render_template('bmw_x6.html')


@app.route('/BMW_X5')
def bmw_x5():  # Регистрация
    return render_template('bmw_x5.html')


@app.route('/BMW_M5_F90')
def bmw_M5_F90():
    return render_template('bmw_m5_f90.html')


@app.route('/BMW_M4')
def bmw_M4():
    return render_template('bmw_m4.html')


@app.route('/BMW_I8')
def bmw_i8():
    return render_template('bmw_i8.html')


if __name__ == '__main__':
    db_session.global_init("db/users.sqlite")
    app.run(port=8080, host='127.0.0.1')
