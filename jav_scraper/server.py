from .models import *

from .manager import Manager

def main():
    # engine = create_engine("sqlite://", echo=True)
    # base.Base.metadata.create_all(engine)
    manager = Manager()
    manager.start()

if __name__ == "__main__":
    main()
