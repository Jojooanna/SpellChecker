from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

engine = create_engine('postgresql://postgres:jojo123@localhost:5432/postgres')
Base = declarative_base()

class Words(Base):
    __tablename__ = 'dictionary'

    codeid = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    words = db.Column(db.ARRAY(String), nullable=False)

    def __init__(self, code, words):
        self.code =code
        self.words = words

class Common(Base):
    __tablename__ = 'common'

    wordid = Column(Integer, primary_key=True)
    words = Column(String)

    def __init__(self, words):
        self.words = words

    # def _
Session = sessionmaker(engine)
session = Session()
