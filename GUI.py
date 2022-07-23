from asyncio.windows_events import NULL
from tkinter import *
from tkinter.ttk import *

class GUI:
    def __init__(self):
        self.nbimage = 1
        self.window = Tk()

        self.percent = StringVar()
        self.text = StringVar()

        self.cb_icon = IntVar()
        self.cb_splash = IntVar()
        self.cb_vertical = IntVar()
        self.cb_spells = IntVar()
        self.cb_champ_data = IntVar()
        
        self.cb_icon.set(1)
        self.cb_splash.set(1)
        self.cb_vertical.set(1)
        self.cb_spells.set(1)
        self.cb_champ_data.set(1)
        
        self.b = 'A'

        c1 = Checkbutton(self.window, text='Champions Icon',variable=self.cb_icon, onvalue=1, offvalue=0)
        c2 = Checkbutton(self.window, text='Champions Splash',variable=self.cb_splash, onvalue=1, offvalue=0)
        c3 = Checkbutton(self.window, text='Champions Vertical',variable=self.cb_vertical, onvalue=1, offvalue=0)
        c4 = Checkbutton(self.window, text='Champions Spells',variable=self.cb_spells, onvalue=1, offvalue=0)
        c5 = Checkbutton(self.window, text='Champions Data',variable=self.cb_champ_data, onvalue=1, offvalue=0)
        
        c1.grid(row=1, column=1)
        c2.grid(row=2, column=1)
        c3.grid(row=3, column=1)
        c4.grid(row=4, column=1)
        c5.grid(row=1, column=2)

        self.bar = Progressbar(self.window,orient=HORIZONTAL,length=300)
        self.bar.grid(row=6, column=1,columnspan=2)

        
        percentLabel = Label(self.window,textvariable=self.percent).grid(row=7, column=1,columnspan=2)
        taskLabel = Label(self.window,textvariable=self.text).grid(row=8, column=1,columnspan=2)
  
    def updateTask(self,strTask,actual):
        self.bar['value']=(actual/self.nbimage)*100
        self.percent.set(str(int((actual/self.nbimage)*100))+"%")
        self.text.set(str(strTask))
        self.window.update_idletasks()

    def setTotalImage(self, nbimg):
        self.nbimage = nbimg

    def getCheckbox(self,item):
        match item:
            case 'cb_icon':
                return self.cb_icon
            case 'cb_splash':
                return self.cb_splash 
            case 'cb_vertical':
                return self.cb_vertical 
            case 'cb_spells':
                return  self.cb_spells
            case 'cb_champ_data':
                return self.cb_champ_data 
            case _:
                return NULL

       
        
       
        