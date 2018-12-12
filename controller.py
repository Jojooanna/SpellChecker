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
    engine = create_engine('postgresql://postgres:jojo123@localhost:5432/fortesting')
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
    print ("No. of FP:", len(self.wrong))

    # UNCOMMENT WHEN READY NA MAG TESTING
    # DON'T UNCOMMENT OMG
    for i in self.wrong:
        transferfromDict(self, i) 
    
    if (self.wrong == []):
        wx.MessageBox("YEY NO MORE WRONG WORDS")
    else:
        self.checkindexCurr = 0
        self.currentword = self.wrong[self.checkindexCurr]
        self.curwordindex = 0 
        self.originaltext.SetValue(self.currentword)
        self.check.Bind(wx.EVT_FIND, self.OnHighlight)

def addCommon(self, i):
    primary, secondary = x.process(i)
    if primary == secondary:
        data = session.query(Common).filter(Common.code == primary).first()
        if data is None:
            dict = Common(code=primary, words=[i])
            session.add(dict)
            session.commit()
        else:
            OnConvertCommon(i)
    else:
        dataPri = session.query(Common).filter(Common.code == primary).first()
        if dataPri is None:
            dictPri = Common(code=primary, words=[i])
            session.add(dictPri)
            session.commit()
        else:
            OnConvertCommon(i)

        dataSec = session.query(Common).filter(Common.code == primary).first()
        if dataSec is None:
            dictSec = Common(code=primary, words=[i])
            session.add(dictSec)
            session.commit()
        else:
            OnConvertCommon(i)

def transferfromDict(self, i):
    # for i in List:
    # converted = ForceToUnicode(i)
    # result = re.sub(r"[^A-Za-z /' -]", "", converted)
    primary, secondary = x.process(i)

    if primary == secondary:
        dictdata = session.query(Words).filter(Words.code==primary).first()
        if dictdata is None:
            pass
        else:
            for j in dictdata.words:
                OnConvertCommon(j)

            session.delete(dictdata)
            session.commit()

    else:
        dictdataPri = session.query(Words).filter(Words.code==primary).first()
        if dictdataPri is None:
            pass
        else:
            for j in dictdataPri.words:
                OnConvertCommon(j)

            session.delete(dictdataPri)
            session.commit()

        dictdataSec = session.query(Words).filter(Words.code==primary).first()
        if dictdataSec is None:
            pass
        else:
            for j in dictdataSec.words:
                OnConvertCommon(j)

            session.delete(dictdataSec)
            session.commit()

def displaySuggestions(self, input):
    priCode, secCode = x.process(input)
    distance = []
    if priCode == secCode:
        # checks at common db first, then dictionary db
        dataCommon = session.query(Common).filter(Common.code == priCode).first()
        if dataCommon is None:
            data = session.query(Words).filter(Words.code == priCode).first()
            if data is None:
                self.notfoundmsg.SetLabel("No suggestions found")
            else:
                self.notfoundmsg.SetLabel("These are the suggestions.")
                for i in data.words:
                    if i in suggestionslist:
                        pass
                    else:
                        suggestionslist.append(i)
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")
            for i in dataCommon.words:
                if i in suggestionslist:
                    pass
                else:
                    suggestionslist.append(i)
    else:
        # checks at common db first, then dictionary db
        dataCommon = session.query(Common).filter(Common.code == priCode).first()
        if dataCommon is None:
            data = session.query(Words).filter(Words.code == priCode).first()
            if data is None:
                self.notfoundmsg.SetLabel("No suggestions found")
            else:
                self.notfoundmsg.SetLabel("These are the suggestions.")
                for i in data.words:
                    if i in suggestionslist:
                        pass
                    else:
                        suggestionslist.append(i)
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")
            for i in dataCommon.words:
                if i in suggestionslist:
                    pass
                else:
                    suggestionslist.append(i)

        # Checks at common db first, then dictionary db
        dataCommon2 = session.query(Common).filter(Common.code == secCode).first()
        if dataCommon2 is None:
            data2 = session.query(Words).filter(Words.code == secCode).first()
            if data2 is None:
                self.notfoundmsg.SetLabel("No suggestions found")
            else:
                self.notfoundmsg.SetLabel("These are the suggestions.")
                for i in data2.words:
                    if i in suggestionslist:
                        pass
                    else:
                        suggestionslist.append(i)
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")
            for i in dataCommon2.words:
                if i in suggestionslist:
                    pass
                else:
                    suggestionslist.append(i)

def displayLevSugg(self, input):
    priCode, secCode = x.process(input)
    distance = []
    if priCode == secCode:
        # Checks at common db first, then dictionary db
        dataCommon = session.query(Common).filter(Common.code == priCode).first()
        if dataCommon is None:
            data = session.query(Words).filter(Words.code == priCode).first()
            if data is None:
                self.notfoundmsg.SetLabel("No suggestions found")
            else:
                self.notfoundmsg.SetLabel("These are the suggestions.")
                for i in data.words:
                    print ("LEVENSHTEIN RESULT:", i, levenshtein(input,i))
                    sortSuggestions(levenshtein(input,i), i)
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")
            for i in dataCommon.words:
                print ("LEVENSHTEIN RESULT:", i, levenshtein(input,i))
                sortSuggestions(levenshtein(input,i), i)
    else:
        # Checks common db first, then dictionary db
        dataCommon = session.query(Common).filter(Common.code == priCode).first()
        if dataCommon is None:
            data = session.query(Words).filter(Words.code == priCode).first()
            if data is None:
                self.notfoundmsg.SetLabel("No suggestions found")
            else:
                self.notfoundmsg.SetLabel("These are the suggestions.")

                for i in data.words:
                    print ("LEVENSHTEIN RESULT:", i, levenshtein(input,i))
                    sortSuggestions(levenshtein(input,i), i)
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")
            for i in dataCommon.words:
                print ("LEVENSHTEIN RESULT:", i, levenshtein(input,i))
                sortSuggestions(levenshtein(input,i), i)

        # Checks common db first, then dictionary db
        dataCommon2 = session.query(Common).filter(Common.code == priCode).first()
        if dataCommon2 is None:
            data2 = session.query(Words).filter(Words.code == secCode).first()
            if data2 is None:
                self.notfoundmsg.SetLabel("No suggestions found")
            else:
                self.notfoundmsg.SetLabel("These are the suggestions.")
                for i in data2.words:
                    print ("LEVENSHTEIN RESULT:", i, levenshtein(input,i))
                    sortSuggestions(levenshtein(input,i), i)
        else:
            self.notfoundmsg.SetLabel("These are the suggestions.")
            for i in dataCommon2.words:
                print ("LEVENSHTEIN RESULT:", i, levenshtein(input,i))
                sortSuggestions(levenshtein(input,i), i)

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
    if distanceinput in sortedDictionary:
        if suggList not in sortedDictionary.values():
            sortedDictionary[distanceinput].append(suggList)
    else:
        sortedDictionary[distanceinput] = [suggList]

# ******************************************************************************************
# PARA AHA GANE NI????
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

