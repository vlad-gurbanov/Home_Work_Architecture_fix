# models.py
from marshmallow import Schema, fields

from app.database import db


# Описываем модель Book
class Book(db.Model):
    # указываем какая у нас таблица
    __tablename__ = 'book'
    # указываем колонки
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    year = db.Column(db.Integer)


# Готовим схему для сериализации и десериализации через маршмалоу
class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    year = fields.Int()


# Описываем модель Author
class Author(db.Model):
    # указываем какая у нас таблица
    __tablename__ = 'author'
    # указываем колонки
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)


# Готовим схему для сериализации и десериализации через маршмалоу
class AuthorSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()