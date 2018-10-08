from model import *
from sqlalchemy import create_engine, select
import wx

def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine("postgresql://postgres:jojo123@localhost:5432/postgres")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = connectToDatabase()

#sa pagsave nis data from dictionary to database !!!! important
with open("dictionary.txt") as f:
    F = f.read().splitlines()
for words in F:
    ed_user = inputWords(word=words)
    session.add(ed_user)
    session.commit()
    print words


#
# List = ['aabot', 'ambot', 'aalisan', 'makapagtatag', 'makakikita', 'makapananghali', 'aalis', 'aabutin', 'makipagkuwentuhan', 'makapagtatag']
#
# wrong = []
#
# for words in List:
#  # ed_user = inputWords(word=words)
#     data = session.query(inputWords).filter(inputWords.word == words).first()
#     print words
#     if data is None:
#         print words
#         wrong.append(words)
#     else:
#         print words
#         # session.add(ed_user)
#         # session.commit()
#         # print "added"
#  #kung wala ang words e append sya sa wrong na list
# print wrong
# # for x in session.query(inputWords):
# #     print x.word
