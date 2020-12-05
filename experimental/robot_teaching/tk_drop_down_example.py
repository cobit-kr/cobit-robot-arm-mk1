from tkinter import *
from tkinter import ttk
import tkinter.messagebox

class App:
    def __init__(self):
        self.master = Tk()
        self.di = {'Asia': ['Japan', 'China', 'Malaysia', 'India', 'Korea',
                            'Vietnam', 'Laos', 'Thailand', 'Singapore',
                            'Indonesia', 'Taiwan'],
                     'Europe': ['Germany', 'France', 'Switzerland'],
                     'Africa': ['Nigeria', 'Kenya', 'Ethiopia', 'Ghana',
                                'Congo', 'Senegal', 'Guinea', 'Mali', 'Cameroun',
                                'Benin', 'Tanzania', 'South Africa', 'Zimbabwe']}
        self.variable_a = StringVar()
        self.frame_optionmenu = ttk.Frame(self.master)
        self.frame_optionmenu.pack()
        options = sorted(self.di.keys())
        self.optionmenu = ttk.OptionMenu(self.frame_optionmenu, self.variable_a, options[0], *options)

        self.variable_a.set('Asia')
        self.optionmenu.pack()
        self.btn = ttk.Button(self.master, text="Submit", width=8, command=self.submit)
        self.btn.pack()

        self.frame_listbox = ttk.Frame(self.master)

        self.frame_listbox.pack(side=RIGHT, fill=Y)
        self.scrollbar = Scrollbar(self.frame_listbox )
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.frame_listbox, selectmode=SINGLE, yscrollcommand=self.scrollbar.set)
        self.variable_a.trace('w', self.updateoptions)

        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()

        #Populate listbox
        for each in self.di[self.variable_a.get()]:
            self.listbox.insert(END, each)
            self.listbox.select_set(0) #This only sets focus on the first item.
        self.listbox.bind("<<ListboxSelect>>", self.OnSelect)

        self.master.mainloop()

    def updateoptions(self, *args):
        #countries = self.di[self.variable_a.get()]
        self.listbox.delete(0, 'end')
        for each in self.di[self.variable_a.get()]:
            self.listbox.insert(END, each)
            self.listbox.select_set(0) #This only sets focus on the first item.
        self.listbox.pack()

    def submit(self, *args):
        var = self.variable_a.get()
        if messagebox.askokcancel("Selection", "Confirm selection: " + var):
            print(var)

    def OnSelect(self, event):
        widget = event.widget
        value = widget.get(widget.curselection()[0])
        print(value)

App()