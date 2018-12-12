from sqlalchemy import create_engine
import wx
from rules import *
from model import *
import re
import numpy as np
from sqlalchemy import func
# -*- encoding: utf-8 -*-
# encoding: utf-8

suggestionslist =[]
sortedDictionary = {}

def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine('postgresql://postgres:mvjunetwo@localhost:5432/spell')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# tiwasunon pa hehe
def ForceToUnicode(text):
    "If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, unicode) else text.decode('utf8')


def spellingCheck(self, List):
    session = connectToDatabase()
    self.wrong = []
    for i in self.List:
        converted = ForceToUnicode(i)
        result = re.sub(r"[^A-Za-z /' -]", "", converted)
        data = session.query(inputWords).filter(func.lower(inputWords.word) == func.lower(result)).first()
        if data is None:
            self.wrong.append(result)
        else:
            print ("spellingCheck results:", result)  # kung wala ang words e append sya sa wrong na list
    # print wrong
    print ("Misspelled words:", self.wrong)

    # UNCOMMENT WHEN READY NA MAG TESTING
    # DON'T UNCOMMENT OMG
    # for i in self.wrong:
    #     addCommon(self, i) 
    
    if (self.wrong == []):
        wx.MessageBox("YEY NO MORE WRONG WORDS")
    else:
        self.checkindexCurr = 0
        self.currentword = self.wrong[self.checkindexCurr]
        self.curwordindex = 0 
        self.originaltext.SetValue(self.currentword)
        self.check.Bind(wx.EVT_FIND, self.OnHighlight)

def addCommon(self, i):
    # for i in List:
    converted = ForceToUnicode(i)
    result = re.sub(r"[^A-Za-z /' -]", "", converted)
    primary, secondary = x.process(result)
    if primary == secondary:
        # print("{}: {}".format(primary, i))
        data = session.query(Common).filter(Common.code == primary).first()
        dictdata = session.query(Words).filter(Words.code == primary).first()
        if data is None:
            dict = Common(code=primary, words=[i])
            session.add(dict)
            session.commit()
            if dictdata is None:
                print ("Misspelled Word doesn't exist.")
            else:
                session.delete(dictdata)
                session.commit()
        else:
            if i in data.words:
                print ("Common Misspelled Word Already Added.")
            else:
                data.words = list(data.words)
                data.words.append(i)
                session.merge(data)
                session.commit()
    else:
        dataPri = session.query(Common).filter(Common.code == primary).first()
        dictdataPri = session.query(Words).filter(Words.code == primary).first()
        if dataPri is None:
            dict = Common(code=primary, words=[i])
            session.add(dict)
            session.commit()
            if dictdataPri is None:
                print ("Misspelled Word doesn't exist.")
            else:
                session.delete(dictdataPri)
                session.commit()
        else:
            if i in dataPri.words:
                print ("Common Misspelled Word Already Added.")
            else:
                dataPri.words = list(dataPri.words)
                dataPri.words.append(i)
                session.merge(dataPri)
                session.commit()

        dataSec = session.query(Common).filter(Common.code == secondary).first()
        dictdataSec = session.query(Words).filter(Words.code == secondary).first()
        if dataSec is None:
            dict = Common(code=secondary, words=[i])
            session.add(dict)
            session.commit()
            if dictdataSec is None:
                print ("Misspelled Word doesn't exist.")
            else:
                session.delete(dictdataSec)
                session.commit()
        else:
            if i in dataSec.words:
                print ("Common Misspelled Word Already Added.")
            else:
                dataSec.words = list(dataSec.words)
                dataSec.words.append(i)
                session.merge(dataSec)
                session.commit()


def displaySuggestions(self, input):
    for x in session.query(inputWords):
        distanceinput = levenshtein(input, x.word)
        if distanceinput <= 3:
            # print x.word.encode('utf-8')
            sortSuggestions(levenshtein(input, x.word), x.word)
            if x.word in suggestionslist:
                pass
            else:
                suggestionslist.append(x.word)
        else:
            pass

def displayCommon(self):
    panel = wx.Panel(self)
    session = connectToDatabase()
    # display all data in words table

    words = []
    for x in session.query(Common):
        for i in x.words:
            print ("Common Words: ", i) # ma print tanan words sa common words
            words.append(i)
    wordsuggest = wx.ListBox(self.panel, choices=words, size=(200, 250), style=wx.LB_HSCROLL)

def deleteDictionary():
    # funtion to delete all common words
    session = connectToDatabase()
    for x in session.query(inputWords):
        session.delete(x)
        session.commit()

def levenshtein(frominput, fromdict):  
    input = len(frominput) + 1
    dict = len(fromdict) + 1
    matrix = np.zeros ((input, dict))
    for x in xrange(input):
        matrix [x, 0] = x
    for y in xrange(dict):
        matrix [0, y] = y

    for x in xrange(1, input):
        for y in xrange(1, dict):
            if frominput[x-1] == fromdict[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    distance = int(matrix[input-1,dict-1])
    return distance

def sortSuggestions(distanceinput, suggList):
    # print ("suggList: ", suggList)
    if distanceinput in sortedDictionary:
        if suggList not in sortedDictionary.values():
            sortedDictionary[distanceinput].append(suggList)
    else:
        sortedDictionary[distanceinput] = [suggList]


