import wx


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        panel = wx.Panel(self)

        menubar = wx.MenuBar()
        NewMenu = wx.Menu()
        ViewMenu = wx.Menu()
        SusMenu = wx.Menu()
        NewMenu.Append(wx.ID_NEW, '&New')
        fileItem = NewMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit application')
        # fileItem1 = NewMenu.Append(wx.ID_EXIT, 'New\tCtrl+F', 'Create New File')

        menubar.Append(NewMenu, '&New')
        menubar.Append(ViewMenu, '&Save')
        menubar.Append(SusMenu, '&sus')
        self.SetMenuBar(menubar)



        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
        # self.Bind(wx.EVT_MENU, self.NewFile, fileItem1)

        wx.TextCtrl(panel, pos = (10,10), size = (500, 450))

        self.SetSize((1200, 700))
        self.SetTitle('Filipino Spelling Checker')
        self.Centre()



    def OnQuit(self, e):
        self.Close()

def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
