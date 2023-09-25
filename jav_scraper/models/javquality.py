from .. import db

class JAVQuality(db.Model):
    __tablename__ = "jav_quality"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    resolution = db.Column(db.String, nullable=False)
    vr = db.Column(db.Boolean, nullable=False)
    uncensored = db.Column(db.Boolean, nullable=False)
