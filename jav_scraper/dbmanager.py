from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

class DBManager():
    _engine = None

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


    def __init__(self):
        self._engine = create_engine('sqlite:///db.sqlite', echo=True)


    def write(self, object):
        session = sessionmaker(bind = self._engine)()
        session.add(object)
        session.commit()
