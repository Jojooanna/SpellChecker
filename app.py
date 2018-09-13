import os
import wx


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.inputtext = wx.TextCtrl(self, size = (800, 650), style=wx.TE_MULTILINE)

        self.InitUI()

    def InitUI(self):

        panel = wx.Panel(self)

        menubar = wx.MenuBar()
        FileMenu = wx.Menu()

        fileNew = FileMenu.Append(wx.ID_NEW, '&New')
        fileOpen = FileMenu.Append(wx.ID_OPEN, '&Open')
        FileMenu.AppendSeparator()

        fileSave = FileMenu.Append(wx.ID_SAVE, '&Save')
        fileSaveAs = FileMenu.Append(wx.ID_SAVEAS, '&Save As')
        FileMenu.AppendSeparator()

        FileMenu.Append(wx.ID_EDIT, '&Rename')
        FileMenu.AppendSeparator()

        fileQuit = FileMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit application')
        # fileItem1 = NewMenu.Append(wx.ID_EXIT, 'New\tCtrl+F', 'Create New File')

        ViewMenu = wx.Menu()

        ViewMenu.Append(wx.ITEM_NORMAL, '&Zoom Out')
        ViewMenu.Append(wx.ITEM_NORMAL, '&Normal')
        ViewMenu.Append(wx.ITEM_NORMAL, '&Zoom In')
        ViewMenu.AppendSeparator()

        ViewMenu.Append(wx.ITEM_NORMAL, '&Full Screen')

        HelpMenu = wx.Menu()

        HelpMenu.Append(wx.ITEM_NORMAL, '&Help')

        menubar.Append(FileMenu, '&File')
        menubar.Append(ViewMenu, '&View')
        menubar.Append(HelpMenu, '&Help')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnNew, fileNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen) #works
        self.Bind(wx.EVT_MENU, self.OnSave, fileSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, fileSaveAs)
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuit)
        # self.Bind(wx.EVT_MENU, self.NewFile, fileItem1)

        self.SetSize((1200, 700))
        self.SetTitle('Filipino Spelling Checker')
        self.Centre()

    def OnNew(self, event):
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
        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            with open(path) as fileobject:
                for line in fileobject:
                    print "You chose %s" % dialog.GetPath()
                    self.inputtext.WriteText(line)

    def OnSave(self, event):
        dlg = wx.FileDialog(
            self, message="Save file as ...",
            defaultFile="", wildcard="txt files (*.txt)|*.txt|All Files (*.*)|*.*", style=wx.FD_SAVE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "You chose the following filename: %s" % path
        dlg.Destroy()

        """self.dirname = ""
        dialog = wx.FileDialog(self, "Save txt file", self.dirname, "",
                                       wildcard="txt files (*.txt)|*.txt|All Files (*.*)|*.*",
                                       style = wx.SAVE | wx.OVERWRITE_PROMPT)"""


    def OnSaveAs(self, event):
        with wx.FileDialog(self, "Save txt file", wildcard="All Files (*.*)|*.*",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.doSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def OnQuit(self, event):
        if wx.MessageBox("Exit SpellChecker?", "Please confirm", wx.YES_NO) != wx.NO:
            self.Close()
            return


def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
