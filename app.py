import os
import wx
import pymysql
import re
import string
import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# -*- encoding: utf-8 -*-
# encoding: utf-8
from model import *
import controller
import rules

engine = create_engine('postgresql://postgres:jojo123@localhost:5432/postgres')
checkindexNew = 0

Session = sessionmaker(bind=engine)
session = Session()


class Example(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.aboutme = wx.MessageDialog(self, "Basic Commands in this Program", "About Spell Checker", wx.OK)
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)

        menubar = wx.MenuBar()
        FileMenu = wx.Menu()

        fileNew = FileMenu.Append(wx.ID_NEW, '&New', "Create New File")
        fileOpen = FileMenu.Append(wx.ID_OPEN, '&Open', "Open File")
        FileMenu.AppendSeparator()

        fileSave = FileMenu.Append(wx.ID_SAVE, '&Save', "Save File")
        fileSaveAs = FileMenu.Append(wx.ID_SAVEAS, '&Save As', "Save File As")
        FileMenu.AppendSeparator()

        fileQuit = FileMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit Program')

        menubar.Append(FileMenu, '&File')
        self.SetMenuBar(menubar)

        # **********************************************************
        # Not important items -- and di sad muwork SO di apilon haha
        # ViewMenu = wx.Menu()
        # ZoomIn = ViewMenu.Append(wx.ITEM_NORMAL, '&Zoom In', "Zoom In")
        # ZoomOut = ViewMenu.Append(wx.ITEM_NORMAL, '&Zoom Out', "Zoom Out")
        # ViewMenu.Append(wx.ITEM_NORMAL, '&Normal')
        # ViewMenu.AppendSeparator()
        # ViewMenu.Append(wx.ITEM_NORMAL, '&Full Screen')
        # HelpMenu = wx.Menu()
        # help = HelpMenu.Append(wx.ID_ABOUT, '&Help')
        # menubar.Append(ViewMenu, '&View')
        # menubar.Append(HelpMenu, '&Help')
        # **********************************************************

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        # self.hbox.AddSpacer(5)

        self.vbox5 = wx.BoxSizer(wx.VERTICAL)
        self.vbox5.AddSpacer(15)
        self.filename = wx.StaticText(self.panel, style=wx.ALIGN_CENTER, label="", size=(900, 30))
        self.inputtext = wx.TextCtrl(self.panel, size=(900, 450), style=wx.TE_MULTILINE | wx.TE_RICH2)
        self.misspellinglabel = wx.StaticText(self.panel, label="Misspelled Words", size=(900, 30))
        self.misspellings = wx.TextCtrl(self.panel, size=(900, 120), style=wx.TE_READONLY | wx.TE_RICH2 | wx.TE_MULTILINE)
        self.vbox5.Add(self.filename, flag=wx.CENTER)
        self.vbox5.Add(self.inputtext, flag=wx.CENTER)
        self.vbox5.Add(self.misspellinglabel, 0, wx.ALL, 10)
        self.vbox5.Add(self.misspellings, flag=wx.CENTER)

        self.hbox.Add(self.vbox5, flag=wx.LEFT)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.vbox1.AddSpacer(45)
        self.check = wx.Button(self.panel, size=(350, 50), label="Check Spelling")
        self.check.SetBackgroundColour("dim grey")
        self.check.SetForegroundColour("white")
        self.check.Bind(wx.EVT_BUTTON, self.OnSpellCheck)
        self.vbox1.Add(self.check, 0, flag=wx.CENTER)

        self.vbox1.AddSpacer(20)
        self.vbox6 = wx.BoxSizer(wx.VERTICAL)

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.AddSpacer(20)
        self.vbox8 = wx.BoxSizer(wx.VERTICAL)

        self.originaltextlabel = wx.StaticText(self.panel, label="From:", size=(50, 30))
        self.checktextlabel = wx.StaticText(self.panel, label="To:", size=(50, 30))
        self.vbox8.Add(self.originaltextlabel, flag=wx.LEFT)
        self.vbox8.Add(self.checktextlabel, flag=wx.LEFT)
        self.hbox1.Add(self.vbox8, flag=wx.CENTER)

        self.vbox9 = wx.BoxSizer(wx.VERTICAL)
        self.originaltext = wx.TextCtrl(self.panel, size=(200, 30), style=wx.TE_READONLY)
        self.suggestions = []
        self.checktext = wx.ComboBox(self.panel, value="", choices=self.suggestions, size=(200, 30))
        self.vbox9.Add(self.originaltext, flag=wx.CENTER)
        self.vbox9.Add(self.checktext, flag=wx.CENTER)
        self.hbox1.Add(self.vbox9, flag=wx.CENTER)


        self.vbox7 = wx.BoxSizer(wx.VERTICAL)
        self.changebtn = wx.Button(self.panel, label="Change", size=(100,30))
        self.changebtn.Bind(wx.EVT_BUTTON, self.Change)
        self.changeallbtn = wx.Button(self.panel, label="Change All", size=(100,30))
        #self.changeallbtn.Bind(wx.EVT_BUTTON, self.OnTest)

        self.vbox7.Add(self.changebtn, flag=wx.RIGHT)
        self.vbox7.Add(self.changeallbtn, flag=wx.RIGHT)
        self.hbox1.Add(self.vbox7, flag=wx.CENTER)
        self.vbox6.Add(self.hbox1, flag=wx.CENTER)

        self.vbox6.AddSpacer(20)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.AddSpacer(70)
        self.notfoundmsg = wx.StaticText(self.panel, label=" ", size=(200, 30))
        self.vbox4 = wx.BoxSizer(wx.VERTICAL)
        self.findnextbtn = wx.Button(self.panel, label="Find Next", size=(100, 30))
        self.findnextbtn.Bind(wx.EVT_BUTTON, self.Next)
        self.previousbtn = wx.Button(self.panel, label="Previous", size=(100, 30))
        self.previousbtn.Bind(wx.EVT_BUTTON, self.Previous)

        self.vbox4.Add(self.findnextbtn, flag=wx.CENTER)
        self.vbox4.Add(self.previousbtn, flag=wx.CENTER)
        self.hbox2.Add(self.notfoundmsg, flag=wx.LEFT)
        self.hbox2.Add(self.vbox4, flag=wx.RIGHT)
        self.vbox6.Add(self.hbox2, flag=wx.CENTER)
        self.vbox6.AddSpacer(20)

        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox3.AddSpacer(60)
        self.vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.wordLabel = wx.StaticText(self.panel, label="Non-sorted Results:", size=(200, 30))
        self.wordsuggest = wx.ListBox(self.panel, choices=self.suggestions, style=wx.LB_HSCROLL, size=(200, 100))
        self.levLabel = wx.StaticText(self.panel, label="Levenshtein Results:", size=(200, 30))
        self.suggestionsLev = []
        self.levSuggest = wx.ListBox(self.panel, choices=self.suggestionsLev, style=wx.LB_HSCROLL, size=(200, 100))
        self.vbox2.Add(self.wordLabel, 0, wx.ALL, 0)
        self.vbox2.Add(self.wordsuggest, flag=wx.CENTER)
        self.vbox2.AddSpacer(20)
        self.vbox2.Add(self.levLabel, 0, wx.ALL, 0)
        self.vbox2.Add(self.levSuggest, flag=wx.CENTER)

        self.vbox3 = wx.BoxSizer(wx.VERTICAL)

        self.ignorebtn = wx.Button(self.panel, label="Ignore", size=(100, 30))
        self.ignorebtn.Bind(wx.EVT_BUTTON, self.OnIgnore)

        self.learnbtn = wx.Button(self.panel, label="Learn", size=(100, 30))
        self.learnbtn.Bind(wx.EVT_BUTTON, self.OnLearn)

        self.vbox3.AddSpacer(30)
        self.vbox3.Add(self.ignorebtn, flag=wx.CENTER)
        self.vbox3.Add(self.learnbtn, flag=wx.CENTER)

        self.hbox3.Add(self.vbox2, flag=wx.LEFT)
        self.hbox3.Add(self.vbox3, flag=wx.RIGHT)

        self.vbox6.Add(self.hbox3, flag=wx.CENTER)
        self.vbox1.Add(self.vbox6, flag=wx.CENTER)
        self.hbox.Add(self.vbox1, flag=wx.RIGHT)

        self.Bind(wx.EVT_LISTBOX, self.OnLevSuggest, self.levSuggest)
        self.Bind(wx.EVT_COMBOBOX, self.OnWordSuggest, self.checktext)
        self.Bind(wx.EVT_MENU, self.OnNew, fileNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen)  # works
        self.Bind(wx.EVT_MENU, self.OnSave, fileSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, fileSaveAs)  # works(.txt)
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuit)  # works

        # **********************************************************
        # Not important items -- and di sad muwork SO di apilon haha
        # self.Bind(wx.EVT_MENU, self.ZoomIn, ZoomIn)  # works
        # self.Bind(wx.EVT_MENU, self.ZoomIn, ZoomOut)  # notworking
        # self.Bind(wx.EVT_MENU, self.OnAbout, help)  # kuwang
        # # self.Bind(wx.EVT_MENU, self.OnDict, dict)
        # **********************************************************

        self.panel.SetSizer(self.hbox)
        self.SetSize((1400, 700))
        self.SetTitle('Filipino Spelling Checker')
        self.Centre()

        self.checktext.Disable()
        self.changebtn.Disable()
        self.changeallbtn.Disable()
        self.findnextbtn.Disable()
        self.previousbtn.Disable()
        self.ignorebtn.Disable()
        self.learnbtn.Disable()

    def OnHide(self, event):
        self.vbox1.Hide(self.vbox6)

    def OnShow(self, event):
        self.vbox1.Show(self.vbox6)

    def OnIgnore(self, event):
        if wx.MessageBox("Remove word?", "Please confirm", wx.YES_NO) != wx.NO:
            self.checkindexCurr = self.wrong.index(self.currentword)
            self.wrong.remove(self.originaltext.GetValue())
            self.originaltext.SetValue(self.wrong[self.checkindexCurr])  # ma change ang original word sa nxt wrong words
            self.currentword = self.wrong[self.checkindexCurr]
            controller.suggestionslist = []
            self.suggestions = []
            controller.sortedDictionary = dict()
            controller.displaySuggestions(self, self.currentword)
            for i in controller.suggestionslist:
                self.suggestions.append(i)
            # for i in controller.sortedDictionary.
            self.wordsuggest.Set(self.suggestions)
            self.levSuggest.Set(self.suggestionsLev)
            self.checktext.Set(self.suggestions)
            self.checktext.SetLabel(self.suggestions[0])

            self.Refresh()

    def OnLearn(self, event):
        input = inputWords(word=self.originaltext.GetValue())
        if input is None:
            result = session.query(inputWords).filter(inputWords.word == input).first()
            if result is None:
                session.add(input)
                session.commit()

                rules.OnConvert(self.originaltext.GetValue())
                if not self.word:
                    wx.MessageBox("No more words.")
                else:
                    self.checkindexCurr = self.wrong.index(self.currentword)
                    self.wrong.remove(self.originaltext.GetValue())
                    self.originaltext.SetValue(self.wrong[self.checkindexCurr])
                    self.currentword = self.wrong[self.checkindexCurr]
                    controller.suggestionslist = []
                    self.suggestions = []
                    controller.sortedDictionary = dict()
                    controller.displaySuggestions(self, self.currentword)
                    for i in controller.suggestionslist:
                        self.suggestions.append(i)
                    self.wordsuggest.Set(self.suggestions)
                    self.levSuggest.Set(self.suggestionsLev)
                    self.checktext.Set(self.suggestions)
                    self.checktext.SetLabel(self.suggestions[0])
            else:
                print ("End of array.")
            wx.MessageBox("Word Added!")
            self.Refresh()

    def OnWordSuggest(self, event):
        self.checktext.SetValue(self.checktext.GetStringSelection())
        self.checktext.SetLabel(self.checktext.GetStringSelection())

    def OnLevSuggest(self, event):
        pass

    def OnTest(self, e):
        checkindexCurr = self.wrong.index(self.checktext.GetValue())
        checkindexNew = checkindexCurr + 1
        self.checktext.SetValue(self.wrong[checkindexNew])
        self.checktext.SetLabel(wrong[checkindexNew])

    def Change(self, e):
        self.selected = self.checktext.GetStringSelection()
        if self.selected == "":
            wx.MessageBox("We can't change something into nothing")
        else:
            self.inputtext.SetValue(self.inputtext.GetValue().replace(self.currentword, self.selected))

            try:
                self.checktext.Clear()
                self.checkindexCurr = self.wrong.index(self.currentword)
                self.wrong.remove(self.currentword)  # self.wrong.pop(self.checkindexCurr)
                self.originaltext.SetValue(self.wrong[self.checkindexCurr]) #ma change ang original word sa nxt wrong words
                self.currentword = self.wrong[self.checkindexCurr]
                # print (self.currentword)
                # print (self.checkindexCurr)
                # print (self.wrong)
                controller.suggestionslist = []
                self.suggestions = []
                controller.displaySuggestions(self, self.currentword)
                for i in controller.suggestionslist:
                    self.suggestions.append(i)
                self.wordsuggest.Set(self.suggestions)
                self.levSuggest.Set(self.suggestionsLev)
                self.checktext.Set(self.suggestions)
                self.checktext.SetLabel(self.suggestions[0])

                self.Refresh()
                #       dapat pa ba ma clear ang selected after ma change?
            except IndexError:
                wx.MessageBox("No more wrong words")
                # eclear pa dapat ang display suggestions

    def Next(self, e):
        try:
            target1 = self.originaltext.GetValue()
            start1 = self.inputtext.GetValue().find(target1)
            position1 = start1 + len(target1)
            self.inputtext.Bind(wx.EVT_SET_FOCUS, self.UnHighlight(start1, position1))

            self.previousbtn.Enable()
            self.checktext.Clear()
            self.checkindexCurr = self.checkindexCurr + 1
            # print self.wrong[self.checkindexCurr]
            # print self.checkindexCurr
            self.originaltext.SetValue(self.wrong[self.checkindexCurr])
            self.currentword = self.wrong[self.checkindexCurr]
            controller.suggestionslist = []
            controller.sortedDictionary = dict()
            self.suggestions = []

            for i in controller.suggestionslist:
                self.suggestions.append(i)

            self.wordsuggest.Set(self.suggestions)
            self.checktext.Set(self.suggestions)

            for k in controller.sortedDictionary.values():
                for j in k:
                    if j in self.suggestionsLev:
                        pass
                    else:
                        self.suggestionsLev.append(j)
            self.levSuggest.Set(self.suggestionsLev)

            if (self.checkindexCurr == len(self.wrong)-1):
                self.findnextbtn.Disable()

            target = self.originaltext.GetValue()
            count = 0
            for i in range(self.inputtext.GetNumberOfLines()):
                if count == 0:
                    line = self.inputtext.GetLineText(i)
                    if target in line:
                        start = self.inputtext.GetValue().find(target)
                        position = start + len(target)
                        self.inputtext.Bind(wx.EVT_SET_FOCUS, self.OnHighlight(start, position))
                        start = 0
                        count = 1
        except IndexError:
            #self.findnextbtn.Disable()
            wx.MessageBox("No more words.")

    def Previous(self, e):
        try:
            target1 = self.originaltext.GetValue()
            start1 = self.inputtext.GetValue().find(target1)
            position1 = start1 + len(target1)
            self.inputtext.Bind(wx.EVT_SET_FOCUS, self.UnHighlight(start1, position1))
            
            self.findnextbtn.Enable()
            self.checktext.Clear()
            self.checkindexCurr = self.checkindexCurr - 1
            self.previousbtn.Enable()
            self.originaltext.SetValue(self.wrong[self.checkindexCurr])
            self.currentword = self.wrong[self.checkindexCurr]
            # print self.wrong[self.checkindexCurr]
            # print self.checkindexCurr
            controller.suggestionslist = []
            controller.sortedDictionary = dict()
            self.suggestions = []
            self.suggestionsLev = []
            controller.displaySuggestions(self, self.currentword)
        
            for i in controller.suggestionslist:
                self.suggestions.append(i)
            self.wordsuggest.Set(self.suggestions)
            self.checktext.Set(self.suggestions)
            self.checktext.SetLabel(self.suggestions[0])
        
            for k in controller.sortedDictionary.values():
                for j in k:
                    if j in self.suggestionsLev:
                        pass
                    else:
                        self.suggestionsLev.append(j)
            self.levSuggest.Set(self.suggestionsLev)

            self.Refresh()
            if (self.checkindexCurr == 0):
                    self.previousbtn.Disable()


            target = self.originaltext.GetValue()
            count = 0
            for i in range(self.inputtext.GetNumberOfLines()):
                if count == 0:
                    line = self.inputtext.GetLineText(i)
                    if target in line:
                        start = self.inputtext.GetValue().find(target)
                        position = start + len(target)
                        self.inputtext.Bind(wx.EVT_SET_FOCUS, self.OnHighlight(start, position))
                        start = 0
                        count = 1

        except IndexError:
            wx.MessageBox("There's no previous word")

    def OnDict(self, e):
        app = wx.App()

        frame = wx.Frame(None, -1, 'win.py')
        frame.SetDimensions(0, 0, 200, 100)

        # Create text input
        dlg = wx.TextEntryDialog(frame, 'Enter some text', 'Text Entry')
        dlg.SetValue("Dictionary Filename")
        btn = wx.Button(frame, label="Modal Dialog", pos=(75, 60))
        btn.Bind(wx.EVT_BUTTON, self.OnOpen)

        if dlg.ShowModal() == wx.ID_OK:
            print('You entered: %s\n' % dlg.GetValue())
        dlg.Destroy()


    def OnSpellCheck(self, e):
        self.value = self.inputtext.GetValue()
        words = self.value.split()
        List = []
        for i in words:
            result = controller.ForceToUnicode(i)
            if result in List:
                continue
            else:
                List.append(i)
        print List

        if not words:
            wx.MessageBox("Please enter something for us to check your work!!")
        else:
            controller.spellingCheck(self, List)
            controller.suggestionslist = []
            controller.sortedDictionary = dict()
            self.suggestions = []
            self.suggestionsLev = []
            controller.displaySuggestions(self, self.currentword)
            for i in controller.suggestionslist:
                self.suggestions.append(i)
            self.wordsuggest.Set(self.suggestions)
            self.checktext.Set(self.suggestions)
            self.checktext.SetLabel("Hello")
            misspelled = []
            for i in self.wrong:
                misspelled.append(controller.ForceToUnicode(i))
            self.misspellings.SetValue(json.dumps(misspelled))

            for k in controller.sortedDictionary.values():
                for j in k:
                    self.suggestionsLev.append(j)
            self.levSuggest.Set(self.suggestionsLev)
        
            self.Refresh()
        
        self.checktext.Enable()
        self.changebtn.Enable()
        self.changeallbtn.Enable()
        self.findnextbtn.Enable()
        self.previousbtn.Enable()
        self.ignorebtn.Enable()
        self.learnbtn.Enable()

        if (self.checkindexCurr == 0):
            self.previousbtn.Disable()

        target = self.originaltext.GetValue()
        print ("target self.originaltext:", target)

        for i in range(self.inputtext.GetNumberOfLines()):
            line = self.inputtext.GetLineText(i)
            if target in line:
                start = self.inputtext.GetValue().find(target)
                position = start + len(target)
                self.inputtext.Bind(wx.EVT_SET_FOCUS, self.OnHighlight(start, position))
                start = 0

        # self.value = str(self.inputtext.GetValue())
        # self.value2 = self.value.split()
        # words = self.value2
        # print (words) # list and words?
        # List = []
        # for i in words:
        #     #returns the position of the manually selected word
        #     #para unta sa pag-highlight
        #     #print (self.inputtext.GetSelection())
        #     if i in List:
        #         continue
        #     else:
        #         List.append(i)
        # print (List)

        # count = 0
        # for i in List: #for phoenics and lev.
        #     count = 0
        #     for j in i:
        #         count = count + 1
        #     print count
        # self.word.SetLabel(self.inputtext)

        # self.notfoundmsg.Hide()


    # def OnFind(self, e):
    #     target = self.originaltext.GetValue()
    #     print ("target self.originaltext:", target)

    #     for i in range(self.inputtext.GetNumberOfLines()):
    #         line = self.inputtext.GetLineText(i)
    #         if target in line:
    #             start = self.inputtext.GetValue().find(target)
    #             position = start + len(target)
    #             self.inputtext.Bind(wx.EVT_SET_FOCUS, self.OnHighlight(start, position))
    #             start = 0

    def OnHighlight(self, start, position):
        self.inputtext.SetStyle(start, position, wx.TextAttr("black", "turquoise"))
        self.inputtext.SetInsertionPoint(start)

    def UnHighlight(self, start, position):
        self.inputtext.SetStyle(start, position, wx.TextAttr("black", "white"))
        self.inputtext.SetInsertionPoint(start)

    def closeButton(self, event):
        print "Button pressed."

    def OnNew(self, event):
        self.inputtext.Clear()
        self.misspellings.Clear()
        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.inputtext.SetFont(font2)
        with wx.FileDialog(self, "Save txt file", wildcard="TXT files (*.txt)|*.txt",
                           style=wx.CREATE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.doSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def OnOpen(self, event):
        self.inputtext.Clear()
        self.misspellings.Clear()
        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        self.pathname = dialog.GetPath()
        if os.path.exists(self.pathname):
            with open(self.pathname) as fileobject:
                for line in fileobject:
                    self.filename.SetLabel(dialog.GetFilename())
                    self.inputtext.WriteText(line)

    def OnSaveAs(self, event):
        self.inputtext.SaveFile()
        dialog = wx.FileDialog(self, "Save txt file", wildcard="Save Files (*.txt) | *.txt | All Files (*.*)|*.*",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        with dialog as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            self.pathname = fileDialog.GetPath()
            try:
                with open(self.pathname, 'w') as file:
                    file.write(self.inputtext.GetValue())
                    file.close()
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % self.pathname)

    def OnSave(self, event):
        savefile = open(self.pathname, 'w')
        savefile.write(self.inputtext.GetValue())
        savefile.close()

    def OnQuit(self, event):
        if wx.MessageBox("Exit SpellChecker?", "Please confirm", wx.YES_NO) != wx.NO:
            self.Close()
            return

    # ******************************************************************
    # def ZoomIn(self, event):
    #     #self.defaultstyle = self.inputtext.GetPointSize()
    #     self.defaultsize = self.defaultstyle.GetFont().GetPointSize()
    #     print(self.defaultsize)
    #
    #     font1 = wx.Font(6, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
    #     self.inputtext.SetFont(font1)
    #
    # def ZoomOut(self, event):
    #     self.inputtext.SetSize(self.inputtext.MaxSize())
    #
    # def OnAbout(self, event):
    #     self.aboutme.ShowModal()
    # ******************************************************************


class Modal(wx.Frame):
    def __init__(self):
        app = wx.App()

        frame = wx.Frame(None, -1, 'win.py')
        frame.SetDimensions(0, 0, 200, 50)

        # Create text input
        dlg = wx.TextEntryDialog(frame, 'Enter some text', 'Text Entry')
        dlg.SetValue("Default")
        if dlg.ShowModal() == wx.ID_OK:
            print('You entered: %s\n' % dlg.GetValue())
        dlg.Destroy()


def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()