import json
import datetime
from sqlalchemy.orm import DeclarativeMeta

from .. import db

BaseModel: DeclarativeMeta = db.Model


class Grab(BaseModel):
    __tablename__ = "grab_history"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    state = db.Column(db.String, nullable=False)

    javmovie_id = db.Column(db.Integer, db.ForeignKey('jav_movie.id'), nullable=False)

    quality_id = db.Column(db.Integer, db.ForeignKey("jav_quality.id"), nullable=True)
    quality = db.relationship("JAVQuality")

    download_page = db.Column(db.String)

    _download_links = db.Column(db.String)
    @property
    def download_links(self):
        return json.loads(self._download_links)
    @download_links.setter
    def download_links(self, link):
        self._download_links = json.dumps(link)
