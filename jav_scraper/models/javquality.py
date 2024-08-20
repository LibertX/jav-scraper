from sqlalchemy.orm import DeclarativeMeta
from .. import db

BaseModel: DeclarativeMeta = db.Model


class JAVQuality(BaseModel):
    __tablename__ = "jav_quality"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    priority = db.Column(db.Integer, nullable=False)

    vr = db.Column(db.Boolean, nullable=False)
    uncensored = db.Column(db.Boolean, nullable=False)

    def_1080p = db.Column(db.Boolean, nullable=False)
    def_4k = db.Column(db.Boolean, nullable=False)
    def_8k = db.Column(db.Boolean, nullable=False)
