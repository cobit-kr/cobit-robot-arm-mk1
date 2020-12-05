import subprocess
import time 
import Tkinter as tk 
import ttk

class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        f0 = ttk.Frame(self)

        self.start_subprocess_btn = ttk.Button(f0, text="Start subprocess", command=self.start_subprocess)
        self.start_subprocess_btn.pack(side='left', padx=10)
        self.start_subprocess_btn.configure(state='enable')

        f0.grid(column=1, row=0, padx=10, pady=10, sticky='w')

    def start_subprocess(self):
        print 'Start subprocess...'
        result = subprocess.check_call(['python', 'tk_teaching_robot.py'])
        if result: 
            print 'Failed'
        else:
            print 'Success'

if __name__ == '__main__':
    root = Gui()
    root.mainloop()





