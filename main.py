import os
from Tkinter import *

root = tk.Tk()
class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

	def openfile(self):
		root.withdraw()
		root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                           filetypes=[("Text Files", "*.txt")])
		print(root.filename)
		
    def createWidgets(self):
        self.NEW = Button(self)
        self.NEW["text"] = "NEW"
        self.NEW["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()