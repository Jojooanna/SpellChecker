from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy.dialects import postgresql as pg

engine = create_engine('postgresql://postgres:jojo123@localhost:5432/fortesting')
Base = declarative_base()

class Words(Base):
    __tablename__ = 'dictionary'

    codeid = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    words = db.Column(pg.ARRAY(db.String), nullable=False)

    def __init__(self, code, words):
        self.code = code
        self.words = words

class Common(Base):
    __tablename__ = 'common'

    codeid = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    words = db.Column(pg.ARRAY(db.String), nullable=False)

    def __init__(self, code, words):
        self.code = code
        self.words = words

    # def _
class inputWords(Base):
    __tablename__ = "words"
    wordid =Column(Integer, primary_key=True)
    word = Column(String)

    def __init__(self, word):
        self.word = word

Session = sessionmaker(engine)
session = Session()
session.commit()
