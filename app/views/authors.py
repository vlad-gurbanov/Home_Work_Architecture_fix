# authors.py
from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import AuthorSchema, Author

# Создание неймспейса.
author_ns = Namespace('authors')

# Схема объект для сериализации и десериализации экземпляров.
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


# Интерфейсы для авторов
@author_ns.route('/')  # на адрес / + authors +/
class AuthorsView(Resource):
    def get(self):
        # направляем get запрос
        all_authors = db.session.query(Author).all()
        return authors_schema.dump(all_authors), 200

    def post(self):
        # направляем новую форму
        req_json = request.json
        new_user = Author(**req_json)
        # запускаем сессию для выполнения запроса
        with db.session.begin():
            # сохраняем нашу книгу
            db.session.add(new_user)
        # отдаем пустой объект и код 201 -
        return "", 201


@author_ns.route('/<int:uid>')
class AuthorView(Resource):
    # get продолжает получать некоторый индетификатор.
    def get(self, uid: int):  # Получение данных
        try:
            # получаем объект, где запись id = uid который мы получили
            author = db.session.query(Author).get(uid)
            # получив сущность мы ее сериализуем и отдаем с кодом 200
            return author_schema.dump(author), 200
        except Exception as e:
            #  выводим для примера текстовое обозначение ошибки и код 404
            return str(e), 404

    # для обновления используем метод put, который принимает uid
    def put(self, uid: int):  # Замена данных
        # получает из базы данных нашу книгу
        author = db.session.query(Author).get(uid)
        # забирает реквест в формате json
        req_jsoon = request.json
        # заменяет эти параметры на то, что нам пришло в реквесте.
        author.first_name = req_jsoon.get('first_name')
        author.last_name = req_jsoon.get('last_name')
        # если все прошло успешно, то выполняем добавление в нашу сессию
        db.session.add(author)
        # коммит для сохранения изменений
        db.session.commit()
        # возвращаем пустую строчку и код 204 как ноу контент
        return '', 204

    def patch(self, uid: int):  # Частичное обновление
        author = db.session.query(Author).get(uid)
        req_json = request.json
        # проверяем если в реквесте есть такое поле
        if 'first_name' in req_json:
            author.first_name = req_json.get('first_name')
        if 'last_name' in req_json:
            author.last_name = req_json.get('last_name')
        # добавляем в сеccию, и записываем добавленное
        db.session.add(author)
        db.session.commit()
        # возвращаем пустую строку и код
        return '', 204

    def delete(self, uid: int):  # Удаление записи
        # Вызываем запись по uid
        user = db.session.query(Author).get(uid)
        # Удаляем полученную запись
        db.session.delete(user)
        # сохраняем удаление
        db.session.commit()

        return '', 204

