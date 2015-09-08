from . import db


class SomeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
