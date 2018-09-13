import os
import wx


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) #style=wx.TE_MULTILINE
        self.inputtext = wx.TextCtrl(self, size = (800, 650))

        self.InitUI()

    def InitUI(self):

        panel = wx.Panel(self)

        menubar = wx.MenuBar()
        FileMenu = wx.Menu()

        FileMenu.Append(wx.ID_NEW, '&New')
        fileItem1 = FileMenu.Append(wx.ID_OPEN, '&Open')
        FileMenu.AppendSeparator()

        FileMenu.Append(wx.ID_SAVE, '&Save')
        FileMenu.Append(wx.ID_SAVEAS, '&Save As')
        FileMenu.AppendSeparator()

        FileMenu.Append(wx.ID_EDIT, '&Rename')
        FileMenu.AppendSeparator()

        fileItem2 = FileMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit application')
        # fileItem1 = NewMenu.Append(wx.ID_EXIT, 'New\tCtrl+F', 'Create New File')

        ViewMenu = wx.Menu()
        SusMenu = wx.Menu()

        menubar.Append(FileMenu, '&File')
        menubar.Append(ViewMenu, '&View')
        menubar.Append(SusMenu, '&sus')
        self.SetMenuBar(menubar)


        self.Bind(wx.EVT_MENU, self.OnOpen)
        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem2)
        # self.Bind(wx.EVT_MENU, self.NewFile, fileItem1)

        self.SetSize((1200, 700))
        self.SetTitle('Filipino Spelling Checker')
        self.Centre()


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
                    self.inputtext.WriteText(line)

    def OnQuit(self, e):
        self.Close()

def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
