from model import *
from sqlalchemy import create_engine

def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine("postgresql://postgres:mvjunetwo@localhost:5432/spell")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def addCommon(List):

    # save common words to database

    session = connectToDatabase()
    user = Common(List)
    session.add(user)
    session.commit()

    print("common words added!")