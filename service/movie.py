# здесь бизнес логика, в виде классов или методов. сюда импортируются DAO классы из пакета dao и модели из dao.model
# некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.
from dao.movie import MovieDao

class MovieService:

    def __init__(self, dao: MovieDao):
        self.dao = dao

    def get_all(self, filters):
        return self.dao.get_all(filters)

    def get_one(self, mid):
        return self.dao.get_by_id(mid)

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        self.dao.update(data)
        return self.dao

    def delete(self, mid):
        self.dao.delete(mid)
