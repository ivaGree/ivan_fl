# Описываем все таблицы в создаваемой БД
# при запуске app.py в первый раз БД будет создана и все таблицы создадутся
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# создаем пустую БД
db = SQLAlchemy()


# Опишем таблицы, которые будут наследоваться от этой пустой БД, которые будут наполнять БД
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='user')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __str__(self):
        return f'Пользователь: {self.email} - Фио: {self.username}'


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zag = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
