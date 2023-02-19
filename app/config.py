# config.py

# Проводим конфигурацию БД. Создаем наши настройки.

class Config:
    DEBUG = True
    SECRET = 'test'   # в конфиг выносят некие секретные данные(пример)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
