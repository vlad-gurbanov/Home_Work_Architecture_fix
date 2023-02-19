# books.py

from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import BookSchema, Book

# Создание неймспейса.
book_ns = Namespace('books')

# БукСхема объект для сериализации и десериализации книг в единственном экземпляре
book_schema = BookSchema()
# Буксхема для сер-ции и дес-ции книг во множественных объектов
books_schema = BookSchema(many=True)


@book_ns.route('/')
class BooksView(Resource):
    def get(self):
        all_books = db.session.query(Book).all()
        return books_schema.dump(all_books), 200

    def post(self):
        req_json = request.json
        new_book = Book(**req_json)
        with db.session.begin():
            db.session.add(new_book)
        return "", 201


@book_ns.route('/<int:uid>')
class BookView(Resource):
    # get продолжает получать некоторый индетификатор
    def get(self, uid: int):   # Получение данных
        # добавляем дополнительную обработку на случай
        # если в базе не найдена запись отдаем 404, если найдена - 200
        try:
            # получаем книгу, где запись id = тому uid который мы получили
            # и one возвращает нам сущность или ошибку
            book = db.session.query(Book).filter(Book.id == uid).one()
            # получив сущность мы ее сериализуем и отдаем с кодом 200
            return book_schema.dump(book), 200
        # в случае ошибки забираем ошибку во временную переменную e
        except Exception as e:
            #  выводим для примера текстовое обзначение ошибки и код 404
            return str(e), 404

    # для обновления используем метод put, который принимает uid
    def put(self, uid: int):  # Замена данных
        # получает из базы данных нашу книгу
        book = db.session.query(Book).get(uid)
        # забирает реквест в формате json
        req_jsoon = request.json
        # заменяет эти параметры на то, что нам пришло в реквесте.
        book.name = req_jsoon.get('name')
        book.author = req_jsoon.get('author')
        book.year = req_jsoon.get('year')
        # если все прошло успешно, то выполняем добавление в нашу сессию
        db.session.add(book)
        # коммит для сохранения изменений
        db.session.commit()
        # возвращаем пустую строчку и код 204 как ноу контент
        return '', 204

    def patch(self, uid: int):  # Частичное обновление
        book = db.session.query(Book).get(uid)
        req_json = request.json
        # проверяем если в реквесте есть такое поле
        if 'name' in req_json:
            # если есть ты мы будем его заменять
            book.name = req_json.get('name')
        if 'author' in req_json:
            book.author = req_json.get('author')
        if 'year' in req_json:
            book.year = req_json.get('year')
        # добавляем в семмию и записываем добавленное
        db.session.add(book)
        db.session.commit()
        # возвращаем пустую строку и код
        return '', 204

    def delete(self, uid: int):  # Удаление записи
        # Вызываем запись по uid
        user = db.session.query(Book).get(uid)
        # Удаляем полученную запись
        db.session.delete(user)
        # сохраняем удаление
        db.session.commit()

        return '', 204

