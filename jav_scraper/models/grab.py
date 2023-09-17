from sqlalchemy import DateTime, String, List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class Grab(Base):
    __tablename__ = "grab_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    javmovie: Mapped["JAVMovie"] = relationship(back_populates="grabs")
    download_page: Mapped[str] = mapped_column(String())

    _download_links: Mapped[str] = mapped_column(String())
    @property
    def download_links(self):
        return self._download_links.split(',')
    @download_links.setter
    def download_links(self, link):
        self._download_links += ',%s' % link
