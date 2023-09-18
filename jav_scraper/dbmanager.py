from sqlalchemy import create_engine

class DBManager():
    _engine = None

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self._engine = create_engine('sqlite:///db.sqlite')
