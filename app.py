import os
import wx
import pymysql
import re
import string
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *
import controller

engine = create_engine('postgresql://postgres:jojo123@localhost:5432/spell')

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

        fileSave = FileMenu.Append(wx.ID_SAVE, '&Save',"Save File")
        fileSaveAs = FileMenu.Append(wx.ID_SAVEAS, '&Save As', "Save File As")
        FileMenu.AppendSeparator()

        fileQuit = FileMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit Program')
        # fileItem1 = NewMenu.Append(wx.ID_EXIT, 'New\tCtrl+F', 'Create New File')

        ViewMenu = wx.Menu()

        ZoomIn = ViewMenu.Append(wx.ITEM_NORMAL, '&Zoom In', "Zoom In")
        ZoomOut = ViewMenu.Append(wx.ITEM_NORMAL, '&Zoom Out', "Zoom Out")

        ViewMenu.Append(wx.ITEM_NORMAL, '&Normal')
        ViewMenu.AppendSeparator()

        ViewMenu.Append(wx.ITEM_NORMAL, '&Full Screen')

        HelpMenu = wx.Menu()

        help = HelpMenu.Append(wx.ID_ABOUT, '&Help')

        menubar.Append(FileMenu, '&File')
        menubar.Append(ViewMenu, '&View')
        menubar.Append(HelpMenu, '&Help')
        self.SetMenuBar(menubar)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.inputtext = wx.TextCtrl(self.panel, size=(900, 600), style=wx.TE_MULTILINE)
        self.check = wx.Button(self.panel, label="Check Spelling")
        self.check.Bind(wx.EVT_BUTTON, self.OnButton)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add((-1,5))
        vbox1.Add(self.inputtext)
        vbox1.Add((-1,5))
        vbox1.Add(self.check, flag=wx.CENTER)
        hbox.Add(vbox1, flag=wx.LEFT)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        vbox2.Add((-1,10))
        previous = wx.Button(self.panel, label="<")
        hbox1.Add(previous, 0, flag=wx.EXPAND)
        # Misspelled word will be displayed here.
        word = wx.StaticText(self.panel, label="jwajja")
        hbox1.Add(word, 1, flag=wx.EXPAND)
        next = wx.Button(self.panel, label=">")
        hbox1.Add(next, 0, flag=wx.EXPAND)

        vbox2.Add(hbox1, flag=wx.CENTER)

        # wordsuggest = wx.ListBox(parent, choices=['word1', 'word2', 'word3', 'word4', 'word5', 'word6', 'word7'], style=wx.LB_HSCROLL)
        # vbox2.Add(wordsuggest, flag=wx.CENTER)

        hbox.Add(vbox2, flag=wx.RIGHT)

        self.Bind(wx.EVT_MENU, self.OnNew, fileNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen) #works
        #self.Bind(wx.EVT_MENU, self.OnSave, fileSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, fileSaveAs)#works(.txt)
        self.Bind(wx.EVT_MENU, self.OnAbout, help) #kuwang
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuit) #works
        # self.Bind(wx.EVT_MENU, self.NewFile, fileItem1)
        self.Bind(wx.EVT_MENU, self.ZoomIn, ZoomIn)#works
        self.Bind(wx.EVT_MENU, self.ZoomIn, ZoomOut)#notworking

        self.panel.SetSizer(hbox)
        self.SetSize((1200, 700))
        self.SetTitle('Filipino Spelling Checker')
        self.Centre()

    def OnButton(self, e):
        self.value = str(self.inputtext.GetValue())
        self.value2 = self.value.split()
        words = self.value2
        print (words) # list and words?
        List = []
        for i in words:
            if i in List:
                continue
            else:
                List.append(i)
        print (List)
        # count = 0
        # for i in List: #for phoenics and lev.
        #     count = 0
        #     for j in i:
        #         count = count + 1
        #     print count
        # self.word.SetLabel(self.inputtext)

        # display all data in words table
        for x in session.query(Words):
            print x.code, x.words

        # save common words to database
        # user = Words("BG", words)
        # user = Common(List)
        # session.add(user)
        # session.commit()
        if not words:
            wx.MessageBox("Please Enter something!!")
        else:
            controller.addCommon(List)
       # delete all in common words after spell check
        # for x in session.query(Common):
        #     session.delete(x)
        #     session.commit()


    def closeButton(self, event):
        print "Button pressed."

    def ZoomIn(self, event):
        self.defaultstyle = wx.inputtext.GetPointSize()
        self.defaultsize = self.defaultstyle.GetFont().GetPointSize()
        print(self.defaultsize)

        font1 = wx.Font(size, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.inputtext.SetFont(font1)

    def ZoomOut(self, event):
            self.inputtext.SetSize(self.inputtext.MaxSize())

    def OnNew(self, event):
        self.inputtext.Clear()
        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.inputtext.SetFont(font2)
        with wx.FileDialog(self, "Save txt file", wildcard = "TXT files (*.txt)|*.txt",
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
        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            with open(path) as fileobject:
                for line in fileobject:
                    print "%s" % dialog.GetPath()
                    self.inputtext.WriteText(line)


    def OnSaveAs(self, event):
        self.inputtext.SaveFile()
        dialog = wx.FileDialog(self, "Save txt file", wildcard="Save Files (*.txt) | *.txt | All Files (*.*)|*.*",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        with dialog as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.inputtext.SaveFile()
                    self.doSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def dosave(self, event):
        savefile = open(self.filename, 'w')
        savefile.write(self.inputtext.GetValue())
        savefile.close()

    def OnQuit(self, event):
        if wx.MessageBox("Exit SpellChecker?", "Please confirm", wx.YES_NO) != wx.NO:
            self.Close()
            return

    def OnAbout(self, event):
        self.aboutme.ShowModal()

def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()