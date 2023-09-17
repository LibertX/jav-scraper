from .models import *
from sqlalchemy import create_engine

if __name__ == "__main__":
    engine = create_engine("sqlite://", echo=True)
    base.Base.metadata.create_all(engine)
