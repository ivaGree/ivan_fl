import os
from db import db, User, News
from forms import LoginForm, RegForm, NewsAddForm
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate

app = Flask(__name__)
# Подключим конфиги
app.config.from_pyfile('config.py')
# Подключаем БД к приложению
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Создадим первого пользователя админа
# Пароль = 123
user = ['admin@admin.ru', 'Иванов',
        'pbkdf2:sha256:600000$Xdql3EcVXV8ZJwyu$db5b37d239956324d68d9616059b9c59534191452d77d05b575af62d12dd83e9',
        'admin']

# Создание БД при первичном запуске '/webapp.db', таблицы которой описаны в 'db.py'
with app.app_context():
    # TODO а где задается название создаваемых таблиц БД?
    db.create_all()
    check_user = User.query.filter(User.email == user[0]).count()
    # Для теста -----------
    # print_user = User.query.filter(User.email == user[0]).first()
    # print(print_user)
    # print(print_user.status)
    # ---------------------
    if not check_user:
        # Добавим пользователя
        add_user = User(
            email=user[0],
            username=user[1],
            password=user[2],
            status=user[3],
        )

        db.session.add(add_user)
        db.session.commit()


@app.route('/')
def index():
    title = 'Главная'
    return render_template('index.html', title=title)


@app.route('/page')
def page():
    title = 'Страничка 2'
    if not current_user.is_authenticated:
        flash('Ошибка! Доступ запрещен!')
        return redirect('/auth')
    return render_template('page.html', title=title)


@app.route('/profile')
def profile():
    title = 'Профиль пользователя'
    if not current_user.is_authenticated:
        flash('Ошибка! Доступ запрещен!')
        return redirect('/auth')
    return render_template('profile.html', title=title)


@app.route('/news')
def news():
    title = 'Новости'
    if not current_user.is_authenticated:
        flash('Ошибка! Доступ запрещен!')
        return redirect('/auth')
    all_news = News.query.order_by(News.published_at.desc()).all()
    return render_template(
        'news.html',
        all_news=all_news,
        title=title,
    )


@app.route('/news_post/<int:id>')
def news_post(id):
    # LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0.
    # TODO как передать в title - Заголовок новости? News.zag
    news = News.query.get(id)
    return render_template(
        'news_post.html',
        news=news,
    )


@app.route('/news_post/<int:id>/del')
def news_del(id):
    news = News.query.get_or_404(id)
    try:
        db.session.delete(news)
        db.session.commit()
        # TODO наверное костыль? но так не работает - return redirect(url_for('news'))
        return redirect('/news')
    # TODO почему ругается на except? хотя код работает
    except:
        flash('Ошибка! При удалении статьи')


@app.route('/news_add', methods=['GET', 'POST'])
def news_add():
    title = 'Добавить новость'
    form = NewsAddForm()
    if request.method == 'POST':
        new_news = News(
            zag=form.zag.data,
            description=form.description.data,
        )
        db.session.add(new_news)
        db.session.commit()
        flash('Новость успешно добавлен!')

    return render_template(
        'news_add.html',
        title=title,
        form=form,
    )


@app.errorhandler(404)
def page_404(error):
    title = 'Ошибка 404'
    return render_template('404.html', title=title)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    title = 'Авторизация'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('profile'))
        flash('Ошибка! Проверьте данные!')
    return render_template(
        'auth.html',
        form=form,
        title=title,
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/users')
@login_required
def users():
    title = 'Список пользователей'
    if current_user.status != 'admin':
        return redirect(url_for('users'))
    users = User.query.all()
    return render_template(
        'users.html',
        users=users,
        title=title,
    )


@app.route('/users_add', methods=['GET', 'POST'])
def users_add():
    title = 'Добавить пользователя'
    form = RegForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                email=form.email.data,
                username=form.username.data,
                status='admin',
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Пользователь успешно добавлен!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Ошибка! в поле {field}: {error}')
    return render_template(
        'users_add.html',
        title=title,
        form=form,
    )


if __name__ == '__main__':
    app.run(debug=True)
