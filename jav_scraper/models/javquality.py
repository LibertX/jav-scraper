from .. import db

class JAVQuality(db.Model):
    __tablename__ = "jav_quality"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
