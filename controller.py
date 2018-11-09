from sqlalchemy import create_engine
import wx
from rules import *
from model import *
import re
from sqlalchemy import func
# -*- encoding: utf-8 -*-
# encoding: utf-8

suggestionslist =[]

def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine('postgresql://postgres:jojo123@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# tiwasunon pa hehe
def ForceToUnicode(text):
    "If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, unicode) else text.decode('utf8')

def addCommon(self, List):

    #/ save common words to database
    # -echeck pa data kung naa na ba sya na common words before sya mag add
    # session = connectToDatabase()
    # words = Common(List)
    # session.add(words)
    # session.commit()
    # print("common words added!")
    # # displayWords(self)
    # spellingCheck(self, List)

    for i in List:
        result = re.sub(r'[^A-Za-z !?@#$%^&*_=+]', "", i)
        input = session.query(Common).filter(Common.words == result).first()
        if input is None:
            result1 = Common(words=result)
            session.add(result1)
        else:
            print ("Common Word Already Added.")
    spellingCheck(self, List)

    for i in List:
        OnConvert(i)


def spellingCheck(self, List):
    session = connectToDatabase()
    self.wrong = []
    for i in List:
        converted = ForceToUnicode(i)
        result = re.sub(r"[^A-Za-z !?@#$%^&*_=+]", "", converted)
        data = session.query(inputWords).filter(func.lower(inputWords.word) == result).first()
        if data is None:
            self.wrong.append(result)
        else:
            print result  # kung wala ang words e append sya sa wrong na list
    # print wrong
    print self.wrong
    if (self.wrong == []):
        wx.MessageBox("YEY NO MORE WRONG WORDS")
    else:
        self.checkindexCurr = 0
        self.currentword = self.wrong[self.checkindexCurr]
        self.originaltext.SetValue(self.currentword)
        self.check.Bind(wx.EVT_FIND, self.OnHighlight)  # HIGHLIGHJUSEYO
        # displaySuggestions(self, self.currentword)
    # primary, secondary = x.process(self.currentword)
    # suggestions = session.query(Words).filter(Words.code == primary)
    # words = []
    #
    # for x.words in suggestions:
    #     words.append(x.words)
    #
    # print primary, secondary
    # print self.words

def displaySuggestions(self, input):
    priCode, secCode = x.process(input)
    data = session.query(Words).filter(Words.code == priCode).first()
    if data is None:
        self.notfoundmsg.SetLabel("No suggestions found")
    else:
        self.notfoundmsg.SetLabel("These are the suggestion")
        for i in data.words:
            if i in suggestionslist:
                pass
            else:
                suggestionslist.append(i)

    data2 = session.query(Words).filter(Words.code == secCode).first()
    if data2 is None:
        self.notfoundmsg.SetLabel("No suggestions found")
    else:
        self.notfoundmsg.SetLabel("These are the suggestion")
        for i in data2.words:
            if i in suggestionslist:
                pass
            else:
                suggestionslist.append(i)


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

