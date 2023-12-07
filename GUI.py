from asyncio.windows_events import NULL
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import os
from pathlib import Path

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
        self.cb_summoners = IntVar()
        self.cb_items = IntVar()
        self.cb_items_s14 = IntVar()
        #self.cb_champ_data = IntVar()
        
        self.cb_icon.set(1)
        self.cb_splash.set(1)
        self.cb_vertical.set(1)
        self.cb_spells.set(1)
        self.cb_summoners.set(1)
        self.cb_items.set(1)
        self.cb_items_s14.set(1)
        #self.cb_champ_data.set(1)
        
        self.b = NULL
        
        indic1 = Label(self.window,text="Choose directory where file download",font=("Arial", 16)).grid(row=0, column=1,columnspan=2)

        self.folder_path = StringVar()
        self.folder_path.set(Path.home() / "Pictures" / "lol_dl_images_data")
        lbl1 = Label(self.window,textvariable=self.folder_path)
        lbl1.grid(row=1, column=1)
        button2 = Button(text="Browse", command=self.browse_button)
        button2.grid(row=1, column=2)

        c1 = Checkbutton(self.window, text='Champions Icon',variable=self.cb_icon, onvalue=1, offvalue=0, command=self.checkCheckboxs)
        c2 = Checkbutton(self.window, text='Champions Splash',variable=self.cb_splash, onvalue=1, offvalue=0, command=self.checkCheckboxs)
        c3 = Checkbutton(self.window, text='Champions Vertical',variable=self.cb_vertical, onvalue=1, offvalue=0, command=self.checkCheckboxs)
        c4 = Checkbutton(self.window, text='Champions Spells',variable=self.cb_spells, onvalue=1, offvalue=0, command=self.checkCheckboxs)
        #c5 = Checkbutton(self.window, text='Champions Data',variable=self.cb_champ_data, onvalue=1, offvalue=0, command=self.checkCheckboxs)
        c6 = Checkbutton(self.window, text='Summoners',variable=self.cb_summoners, onvalue=1, offvalue=0, command=self.checkCheckboxs)
        c7 = Checkbutton(self.window, text='Items',variable=self.cb_items, onvalue=1, offvalue=0, command=self.checkCheckboxs)
        c8 = Checkbutton(self.window, text='Items S14',variable=self.cb_items_s14, onvalue=1, offvalue=0, command=self.checkCheckboxs)

        indic1 = Label(self.window,text="Select what ressources to download",font=("Arial", 16)).grid(row=2, column=1,columnspan=2)

        c1.grid(row=3, column=1)
        c2.grid(row=4, column=1)
        c3.grid(row=5, column=1)
        c4.grid(row=6, column=1)
        #c5.grid(row=3, column=2)
        c6.grid(row=3, column=2)
        c7.grid(row=4, column=2)
        c8.grid(row=5, column=2)
        self.bar = Progressbar(self.window,orient=HORIZONTAL,length=400)
        self.bar.grid(row=8, column=1,columnspan=2)

        
        percentLabel = Label(self.window,textvariable=self.percent).grid(row=9, column=1,columnspan=2)
        taskLabel = Label(self.window,textvariable=self.text).grid(row=10, column=1,columnspan=2)
  
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
            case 'cb_summoners':
                return self.cb_summoners
            case 'cb_items':
                return self.cb_items
            case 'cb_items_s14':
                return self.cb_items_s14
            case _:
                return NULL

    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename =  filedialog.askdirectory()
        self.folder_path.set(filename)
        print(filename)
        
       
    def checkCheckboxs(self):
        #a = self.cb_icon.get() + self.cb_splash.get() + self.cb_vertical.get() + self.cb_spells.get() + self.cb_champ_data.get()
        a = self.cb_icon.get() + self.cb_splash.get() + self.cb_vertical.get() + self.cb_spells.get() + self.cb_summoners.get() + self.cb_items.get() + self.cb_items_s14.get()
        if a == 0:
            self.b["state"] = "disabled"
        else:
            self.b["state"] = "enabled"