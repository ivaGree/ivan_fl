from datetime import timedelta
import os

basedir = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(basedir, '..', 'webapp.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# TODO тут точно нужен LOGIN_MESSAGE ?
LOGIN_MESSAGE = 'Вам доступ запрещен!'
REMEMBER_COOKIE_DURATION = timedelta(days=30)

# Генерация SECRET_KEY в Python console
# import os
# os.urandom(20).hex()
SECRET_KEY = 'eb004eb8525a01513536f9e419e25f5f990afcff'
