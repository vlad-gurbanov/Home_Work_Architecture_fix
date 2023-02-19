# main.py

# Импорт необходимых библиотек
from flask import Flask
from flask_restx import Api

# импортируем класс Config
from app.config import Config
# импортируем db из нашего нового файла
from app.database import db
# подключаем наши модели для работы функции def load_data()
from app.models import Book, Author
# подключаем namespace book_ns, author_ns
from app.views.authors import author_ns
from app.views.books import book_ns


# def create_app() - создает приложение и возвращает его.
# Передадим функции аргумент. Научим ее работать с конфиг.
def create_app(config: Config) -> Flask:
    # создаем app, называем ее application что бы оно не пересекалось с app
    application = Flask(__name__)
    # создаем конфигурацию, вызвав у нее специальный метод from_object
    application.config.from_object(config)  # это и есть наш конфиг класса class Config
    # Применение конфигурации которую мы настроили выше, чтобы Flask обновил ее по всему приложению.
    application.app_context().push()
    return application


# Конфигурируем создание объекта db = SQLAlchemy(). Связь расположения объектов.
def configure_app(application: Flask):
    # подключает базу данных.
    db.init_app(application)
    # создаем объект API.
    api = Api(app)
    # добавление неймспейсов, которые нам будут переданы.
    api.add_namespace(book_ns)  # 'books'
    api.add_namespace(author_ns)  # 'authors'


def load_data():
    # Подготовка данных в виде сущностей от класса моделей
    b1 = Book(id=1, name="Harry Potter", year=2000)
    b2 = Book(id=2, name="Le Comte de Monte-Cristo", year=1844)

    a1 = Author(id=1, first_name="Joan", last_name="Routing")
    a2 = Author(id=2, first_name="Alexander", last_name="Dumas")

    # Создаем необходимые таблицы
    db.create_all()

    # При помощи открытия сессии сохраняем наши книги и авторов в базе
    with db.session.begin():
        db.session.add_all([a1, a2])
        db.session.add_all([b1, b2])


# Запуск приложения. Если файл исполняемый:
if __name__ == '__main__':
    # Загружаем конфигурацию.
    app_config = Config()  # здесь храниться конфигурация.
    # Создаем приложение. Передаем в функцию 'создания приложения' - 'экземпляр класса конфигурации'.
    app = create_app(app_config)  # здесь храниться приложение.

    # вызываем метод configure_app() что бы метод заработал (конфигурируем приложение).
    configure_app(app)  # передаем ему приложение.
    # загрузка данных для создания таблиц.
    load_data()

    # Запускаем приложение.
    app.run()
