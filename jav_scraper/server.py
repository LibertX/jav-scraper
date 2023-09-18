from .models import *
from .manager import Manager
from . import app
from . import db
from . import routes

def main():
    manager = Manager()
    manager.daemon = True
    manager.start()
    app.run()

if __name__ == "__main__":
    main()
