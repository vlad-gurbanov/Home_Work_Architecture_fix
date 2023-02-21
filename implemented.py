# файл для создания DAO и сервисов чтобы импортировать их везде

from dao.movie import MovieDao
from dao.genre import GenreDao
from dao.director import DirectorDao
from service.movie import MovieService
from service.genre import GenreService
from service.director import DirectorService

from setup_db import db

movie_dao = MovieDao(session=db.session)
movie_service = MovieService(dao=movie_dao)

genre_dao = GenreDao(session=db.session)
genre_service = GenreService(dao=genre_dao)

director_dao = DirectorDao(session=db.session)
director_service = DirectorService(dao=director_dao)