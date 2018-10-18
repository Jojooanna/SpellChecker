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

engine = create_engine('postgresql://postgres:jojo123@localhost:5432/postgres')

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

        # dict = FileMenu.Append(wx.ITEM_NORMAL, '&Dict',"Dictionary")
        # FileMenu.AppendSeparator()

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

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.hbox.AddSpacer(10)

        self.vbox5 = wx.BoxSizer(wx.VERTICAL)
        self.vbox5.AddSpacer(15)
        self.filename = wx.StaticText(self.panel, style=wx.ALIGN_CENTER, label="Filename", size=(900,30))
        self.inputtext = wx.TextCtrl(self.panel, size=(900, 600), style=wx.TE_MULTILINE)
        self.vbox5.Add(self.filename, flag=wx.CENTER)
        self.vbox5.Add(self.inputtext, flag=wx.CENTER)

        self.hbox.Add(self.vbox5, flag=wx.LEFT)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.vbox1.AddSpacer(45)
        self.check = wx.Button(self.panel, size=(300,50), label="Check Spelling")
        self.check.SetBackgroundColour("dim grey")
        self.check.SetForegroundColour("white")
        self.check.Bind(wx.EVT_BUTTON, self.OnButton)
        self.vbox1.Add(self.check, 0,flag=wx.CENTER)

        self.vbox1.AddSpacer(10)
        self.vbox6 = wx.BoxSizer(wx.VERTICAL)
        #dapat ma-hide ang mga items sa vbox6 kung wa pa naclick ang "CheckSpelling" nga button

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.AddSpacer(10)
        self.checktext = wx.TextCtrl(self.panel,size=(200,30),)
        self.vbox7 = wx.BoxSizer(wx.VERTICAL)
        self.changebtn = wx.Button(self.panel, label="Change", size=(100,30))
        #self.changebtn.Bind(wx.EVT_BUTTON, self.OnTest)
        self.changeallbtn = wx.Button(self.panel, label="Change All", size=(100,30))
        #self.changeallbtn.Bind(wx.EVT_BUTTON, self.OnTest)

        self.hbox1.Add(self.checktext, flag=wx.LEFT)
        self.vbox7.Add(self.changebtn, flag=wx.RIGHT)
        self.vbox7.Add(self.changeallbtn, flag=wx.RIGHT)
        self.hbox1.Add(self.vbox7, flag=wx.CENTER)
        self.vbox6.Add(self.hbox1, flag=wx.CENTER)

        self.vbox6.AddSpacer(10)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.AddSpacer(10)
        self.notfoundmsg = wx.StaticText(self.panel, label="The word was not found.",size=(200,30))
        self.vbox4 = wx.BoxSizer(wx.VERTICAL)
        self.findnextbtn = wx.Button(self.panel, label="Find Next", size=(100,30))
        self.findnextbtn.Bind(wx.EVT_BUTTON, self.OnTest)
        self.previousbtn = wx.Button(self.panel, label="Previous", size=(100,30))
        self.previousbtn.Bind(wx.EVT_BUTTON, self.OnTest)
        self.vbox4.Add(self.findnextbtn, flag=wx.CENTER)
        self.vbox4.Add(self.previousbtn, flag=wx.CENTER)
        self.hbox2.Add(self.notfoundmsg, flag=wx.LEFT)
        self.hbox2.Add(self.vbox4, flag=wx.RIGHT)
        self.vbox6.Add(self.hbox2, flag=wx.CENTER)
        self.vbox6.AddSpacer(10)

        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox3.AddSpacer(10)
        self.vbox2 = wx.BoxSizer(wx.VERTICAL)
        words = ['word1', 'word2', 'word3', 'word4', 'word5', 'word6', 'word7']
        self.wordsuggest = wx.ListBox(self.panel, choices=words, style=wx.LB_HSCROLL,size=(200,100))
        self.vbox2.Add(self.wordsuggest, flag=wx.CENTER)

        self.vbox3 = wx.BoxSizer(wx.VERTICAL)
        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.ignorebtn = wx.Button(self.panel, label="Ignore", size=(100,30))
        self.ignorebtn.Bind(wx.EVT_BUTTON, self.OnTest)
        self.learnbtn = wx.Button(self.panel, label="Learn", size=(100,30))
        self.learnbtn.Bind(wx.EVT_BUTTON, self.OnTest)
        self.hbox4.Add(self.ignorebtn, flag=wx.CENTER)
        self.hbox5.Add(self.learnbtn, flag=wx.CENTER)
        self.vbox3.Add(self.hbox4, flag=wx.CENTER)
        self.vbox3.Add(self.hbox5, flag=wx.CENTER)

        self.hbox3.Add(self.vbox2, flag=wx.LEFT)
        self.hbox3.Add(self.vbox3, flag=wx.RIGHT)

        self.vbox6.Add(self.hbox3, flag=wx.CENTER)
        self.vbox1.Add(self.vbox6, flag=wx.CENTER)
        self.hbox.Add(self.vbox1, flag=wx.RIGHT)

        self.Bind(wx.EVT_LISTBOX, self.OnWordSuggest, self.wordsuggest)
        self.Bind(wx.EVT_MENU, self.OnNew, fileNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen) #works
        #self.Bind(wx.EVT_MENU, self.OnSave, fileSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, fileSaveAs)#works(.txt)
        self.Bind(wx.EVT_MENU, self.OnAbout, help) #kuwang
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuit) #works
        # self.Bind(wx.EVT_MENU, self.NewFile, fileItem1)
        self.Bind(wx.EVT_MENU, self.ZoomIn, ZoomIn)#works
        self.Bind(wx.EVT_MENU, self.ZoomIn, ZoomOut)#notworking
        # self.Bind(wx.EVT_MENU, self.OnDict, dict)

        self.panel.SetSizer(self.hbox)
        self.SetSize((1200, 700))
        self.SetTitle('Filipino Spelling Checker')
        self.Centre()

    def OnWordSuggest(self, event):
        self.selected = self.wordsuggest.GetStringSelection()
        self.checktext.SetValue(self.selected)

    def OnTest(self, e):
        checkindexCurr = self.wrong.index(self.checktext.GetValue())
        checkindexNew = checkindexCurr + 1
        self.checktext.SetValue(self.wrong[checkindexNew])


        # self.checktext.SetValue(self.wrong[0])

    # def OnDict(self, e):
    #     app = wx.App()
    #
    #     frame = wx.Frame(None, -1, 'win.py')
    #     frame.SetDimensions(0, 0, 200, 100)
    #
    #     # Create text input
    #     dlg = wx.TextEntryDialog(frame, 'Enter some text', 'Text Entry')
    #     dlg.SetValue("Dictionary Filename")
    #     btn = wx.Button(frame, label="Modal Dialog", pos=(75,60))
    #     btn.Bind(wx.EVT_BUTTON, self.OnOpen)
    #
    #     if dlg.ShowModal() == wx.ID_OK:
    #         print('You entered: %s\n' % dlg.GetValue())
    #     dlg.Destroy()

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

        if not words:
            wx.MessageBox("Please enter something for us to check your work!!")
        else:
            controller.addCommon(self, words)


    def closeButton(self, event):
        print "Button pressed."

    def ZoomIn(self, event):
        self.defaultstyle = self.inputtext.GetPointSize()
        self.defaultsize = self.defaultstyle.GetFont().GetPointSize()
        print(self.defaultsize)

        font1 = wx.Font(6, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
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

    def onButton(event):
        print "Button pressed."



def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()