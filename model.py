from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:mvjunetwo@localhost:5432/spell')
Base = declarative_base()

class Words(Base):
    __tablename__ = 'words'

    codeid =Column(Integer, primary_key=True)
    code = Column(String)
    words = Column(String)

    def __init__(self, code, words,codeid):

        self.code =code
        self.words = words
        self.codeid =codeid

Session = sessionmaker(engine)
session = Session()
