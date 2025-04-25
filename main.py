import secrets
from flask import Flask, render_template, redirect, request, make_response, session, abort
from data import db_session
from data.users import User
from data.stores import Story
from forms.login_form import LoginForm
from forms.stores import StoresForm
from forms.registerform import RegisterForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
db_session.global_init("db/blogs.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        story = db_sess.query(Story).filter(
            (Story.user == current_user) | (Story.is_private != True))
    else:
        story = db_sess.query(Story).filter(Story.is_private != True)
    return render_template("index.html", story=story)


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



@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
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


@app.route('/story',  methods=['GET', 'POST'])
@login_required
def add_story():
    form = StoresForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        stores = Story()
        stores.title = form.title.data
        stores.content = form.content.data
        stores.is_private = form.is_private.data
        current_user.story.append(stores)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('stores.html', title='Добавление истории',
                           form=form)


@app.route('/story/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_story(id):
    form = StoresForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        stores = db_sess.query(Story).filter(Story.id == id,
                                          Story.user == current_user
                                          ).first()
        if stores:
            form.title.data = stores.title
            form.content.data = stores.content
            form.is_private.data = stores.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        stores = db_sess.query(Story).filter(Story.id == id,
                                          Story.user == current_user
                                          ).first()
        if stores:
            stores.title = form.title.data
            stores.content = form.content.data
            stores.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('stores.html',
                           title='Редактирование истории',
                           form=form
                           )

@app.route('/story_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def story_delete(id):
    db_sess = db_session.create_session()
    stores = db_sess.query(Story).filter(Story.id == id,
                                      Story.user == current_user
                                      ).first()
    if stores:
        db_sess.delete(stores)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/read',  methods=['GET', 'POST'])
@login_required
def read_story():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        story = db_sess.query(Story).filter(
            (Story.user == current_user) | (Story.is_private != True))
    else:
        story = db_sess.query(Story).filter(Story.is_private != True)
    return render_template("read.html", story=story)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
