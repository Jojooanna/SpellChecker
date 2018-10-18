from model import *
from sqlalchemy import create_engine
import wx

def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine("postgresql://postgres:jojo123@localhost:5432/postgres")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def addCommon(self, List):

    #/ save common words to database
    # -echeck pa data kung naa na ba sya na common words before sya mag add
    session = connectToDatabase()
    words = Common(List)
    session.add(words)
    session.commit()
    print("common words added!")
    # displayWords(self)
    spellingCheck(self, List)

def spellingCheck(self, List):
    session = connectToDatabase()
    self.wrong = []
    for i in List:
        data = session.query(inputWords).filter(inputWords.word == i).first()
        if data is None:
            self.wrong.append(i)
        else:
            print i  # kung wala ang words e append sya sa wrong na list
    # print wrong
    print self.wrong
    self.checktext.SetValue(self.wrong[0])


def displayCommon(self):

    panel = wx.Panel(self)

    session = connectToDatabase()
    # display all data in words table

    words = []
    for x in session.query(Common):
        for i in x.words:
            print i # ma print tanan words sa common words [u'he]
            words.append(i)
    wordsuggest = wx.ListBox(self.panel, choices=words, size=(200, 250), style=wx.LB_HSCROLL)
    # vbox2.Add(wordsuggest, flag=wx.CENTER)

def deleteDictionary():

    # funtion to delete all common words

    session = connectToDatabase()
    for x in session.query(inputWords):
        session.delete(x)
        session.commit()
