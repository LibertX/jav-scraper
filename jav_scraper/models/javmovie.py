from sqlalchemy.orm import Mapped
from .. import db

class JAVMovie(db.Model):
    __tablename__ = "jav_movie"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    code: Mapped[str] = db.Column(db.String, nullable=False)
    grabs = db.relationship('Grab', backref='jav_movie', cascade="all, delete-orphan", lazy=True)

