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
sortedDictionary = dict()

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


def spellingCheck(self, List):
    session = connectToDatabase()
    self.wrong = []
    for i in List:
        converted = ForceToUnicode(i)
        result = re.sub(r"[^A-Za-z -@#$%^&*_=+]", "", converted)
        data = session.query(inputWords).filter(func.lower(inputWords.word) == result).first()
        if data is None:
            self.wrong.append(result)
        else:
            print ("spellingCheck results:", result)  # kung wala ang words e append sya sa wrong na list
    # print wrong
    print ("Misspelled words:", self.wrong)
    addCommon(self, self.wrong) 
    if (self.wrong == []):
        wx.MessageBox("YEY NO MORE WRONG WORDS")
    else:
        self.checkindexCurr = 0
        self.currentword = self.wrong[self.checkindexCurr]
        self.originaltext.SetValue(self.currentword)
        self.check.Bind(wx.EVT_FIND, self.OnHighlight)  # HIGHLIGHTJUSEYO
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


def addCommon(self, List):
    for i in List:
        converted = ForceToUnicode(i)
        result = re.sub(r'[^A-Za-z -@#$%^&*_=+]', "", converted)
        priCode, secCode = x.process(result)
        if priCode == secCode:
            data = session.query(Common).filter(Common.code == priCode).first()
            dictdata = session.query(Words).filter(Words.code == priCode).first()
            if data is None:
                commmondict = Common(code=priCode, words=[result])
                session.add(commondict)

                session.delete(dictdata)
                session.commit()
            else:
                print ("Common Misspelled Word Already Added.")
        else: 
            data1 = session.query(Common).filter(Common.code == priCode).first()
            dictdata1 = session.query(Words).filter(Words.code == priCode).first()

            data2 = session.query(Common).filter(Common.code == secCode).first()
            dictdata2 = session.query(Words).filter(Words.code == secCode).first()

            if data1 is None:
                commondict1 = Common(code=priCode, words=[result])
                session.add(commondict1)

                session.delete(dictdata1)
                session.commit()
            elif data2 is None:
                commondict2 = Common(code=secCode, words=[result])
                session.add(commondict2)

                session.delete(dictdata2)
                session.commit()
            else:
                print ("Common Misspelled Word Already Added.")

def displaySuggestions(self, input):
    priCode, secCode = x.process(input)
    distance = []
    if priCode == secCode:
        data = session.query(Words).filter(Words.code == priCode).first()
        if data is None:
            self.notfoundmsg.SetLabel("No suggestions found")
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")
            for i in data.words:
                print ("LEVENSHTEIN RESULT:", levenshtein(input,i))
                sortSuggestions(levenshtein(input,i), i)
                if i in suggestionslist:
                    pass
                else:
                    suggestionslist.append(i)
    else:
        data = session.query(Words).filter(Words.code == priCode).first()
        if data is None:
            self.notfoundmsg.SetLabel("No suggestions found")
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")

            for i in data.words:
                print ("LEVENSHTEIN RESULT:", levenshtein(input,i))
                sortSuggestions(levenshtein(input,i), i)
                if i in suggestionslist:
                    pass
                else:
                    suggestionslist.append(i)

        data2 = session.query(Words).filter(Words.code == secCode).first()
        if data2 is None:
            self.notfoundmsg.SetLabel("No suggestions found")
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")
            for i in data2.words:
                print ("LEVENSHTEIN RESULT:", levenshtein(input,i))
                sortSuggestions(levenshtein(input,i), i)
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

    print ("suggList: ", suggList)
    if distanceinput in sortedDictionary:
        if suggList not in sortedDictionary.values():
            sortedDictionary[distanceinput].append(suggList)
    else:
        sortedDictionary[distanceinput] = [suggList]



