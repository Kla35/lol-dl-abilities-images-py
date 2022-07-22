from tkinter import *
from tkinter.ttk import *

class GUI:
    def __init__(self,nbimage):
        self.nbimage = nbimage
        self.window = Tk()

        self.percent = StringVar()
        self.text = StringVar()

        self.bar = Progressbar(self.window,orient=HORIZONTAL,length=300)
        self.bar.pack(pady=1)

        percentLabel = Label(self.window,textvariable=self.percent).pack()
        taskLabel = Label(self.window,textvariable=self.text).pack()
  
    def updateTask(self,strTask,actual):
        self.bar['value']=(actual/self.nbimage)*100
        self.percent.set(str(int((actual/self.nbimage)*100))+"%")
        self.text.set(str(strTask))
        self.window.update_idletasks()
