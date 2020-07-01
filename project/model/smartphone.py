from project import db


class Smartphone(db.Model):
    __tablename__ = "smartphone"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)

