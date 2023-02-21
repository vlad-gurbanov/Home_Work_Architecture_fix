from dao.model.genre import Genre


class GenreDao:
    def __init__(self, session):
        self.session = session
        self.model = Genre

    def get_by_id(self, gid):
        return self.session.query(self.model).get(gid)

    def get_all(self):
        return self.session.query(self.model).all()

    def create(self, data):
        genre = self.model(**data)
        self.session.add(genre)
        self.session.comit()
        return genre

    def delete(self, gid):
        genre = self.get_by_id(gid)
        self.session.delete(genre)
        self.session.comit()

    def update(self, data):
        genre = self.get_by_id(data['id'])
        genre.name = data['name']

        self.session.add(genre)
        self.session.comit()