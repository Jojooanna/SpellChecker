import os
import wx
#import sql

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.inputtext = wx.TextCtrl(self, size = (800, 640), style=wx.TE_MULTILINE)
        self.aboutme = wx.MessageDialog(self, "Basic Commands in this Program", "About Spell Checker", wx.OK)
        self.InitUI()

    def InitUI(self):

        panel = wx.Panel(self)

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

        ZoomIn = ViewMenu.Append(wx.ITEM_NORMAL, '&Zoom In')
        Normal = ViewMenu.Append(wx.ITEM_NORMAL, '&Normal')
        ZoomOut = ViewMenu.Append(wx.ITEM_NORMAL, '&Zoom Out')

        ViewMenu.AppendSeparator()

        ViewMenu.Append(wx.ITEM_NORMAL, '&Full Screen')

        HelpMenu = wx.Menu()

        help = HelpMenu.Append(wx.ID_ABOUT, '&Help')

        menubar.Append(FileMenu, '&File')
        menubar.Append(ViewMenu, '&View')
        menubar.Append(HelpMenu, '&Help')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnNew, fileNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen) #works
        self.Bind(wx.EVT_MENU, self.OnSave, fileSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, fileSaveAs) #works(.txt)
        self.Bind(wx.EVT_MENU, self.OnAbout, help) #kuwang
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuit) #works
        # self.Bind(wx.EVT_MENU, self.NewFile, fileItem1)

        # self.Bind(wx.EVT_MENU, self.ZoomIn, ZoomIn) #works
        # self.Bind(wx.EVT_MENU, self.Normal, Normal)
        # self.Bind(wx.EVT_MENU, self.ZoomOut, ZoomOut) #notworking

        self.SetSize((1200, 700))
        self.SetTitle('Filipino Spelling Checker')
        self.Centre()

    def OnNew(self, event):
        self.inputtext.Clear()
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

    def OnSave(self, event):
        self.inputtext.SaveFile()

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
                    #self.inputtext.SaveFile()
                    self.doSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def OnQuit(self, event):
        if wx.MessageBox("Exit SpellChecker?", "Please confirm", wx.YES_NO) != wx.NO:
            self.Close()
            return

    def OnAbout(self, event):
        self.aboutme.ShowModal()

    # def ZoomIn(self, event):
    #     font = wx.Font(24, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
    #     self.inputtext.SetFont(font)
    #
    # def Normal(self, event):
    #     font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
    #     self.inputtext.SetFont(font)
    #
    # def ZoomOut(self, event):
    #     font = wx.Font(6, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
    #     self.inputtext.SetFont(font)

def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
