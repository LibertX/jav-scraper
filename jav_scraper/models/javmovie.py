from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from . import Base

if TYPE_CHECKING:
    from . import Grab, JAVQuality

class JAVMovie(Base):
    __tablename__ = "jav_movie"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String())
    status: Mapped[str] = mapped_column(String())

    quality_id: Mapped[int] = mapped_column(Integer, ForeignKey("jav_quality.id"))
    quality: Mapped["JAVQuality"] = relationship("JAVQuality")

    grabs: Mapped[List["Grab"]] = relationship()
