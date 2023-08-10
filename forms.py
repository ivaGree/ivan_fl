from db import User
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError


class LoginForm(FlaskForm):
    email = StringField(
        'Почта: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'type': 'email'},
    )
    password = PasswordField(
        'Пароль: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'type': 'password'},
    )
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={'class': 'form-check-input', 'type': 'checkbox'}
    )
    submit = SubmitField(
        'Войти',
        render_kw={'class': 'btn btn-success'},
    )

    # def validate_email(self, email):
    #     count_users = User.query.filter(User.email == email.data).count()
    #     if count_users:
    #         raise ValidationError('Пользователь с таким емэйлом уже существует!')


class RegForm(FlaskForm):
    email = StringField(
        'Почта: ',
        validators=[DataRequired(), Email('Это не емэйл!')],
        render_kw={'class': 'form-control'},
    )
    username = StringField(
        'Имя: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    password = PasswordField(
        'Пароль: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    password2 = PasswordField(
        'Повторите пароль: ',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField(
        'Зарегистрировать',
        render_kw={'class': 'btn btn-success'},
    )

    def validate_email(self, email):
        count_users = User.query.filter(User.email == email.data).count()
        if count_users:
            raise ValidationError('Пользователь с таким емэйлом уже существует!')

class NewsAddForm(FlaskForm):
    zag = StringField(
        'Заголовок: ',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    description = StringField(
        'Текст новости: ',
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField(
        'Добавить',
        render_kw={'class': 'btn btn-success'},
    )