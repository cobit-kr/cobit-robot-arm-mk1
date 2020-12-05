from Tkinter import *

root = Tk()

left = Frame(root)
right = Frame(root)

t_start = Text(left, width=20)
t_start.pack(side=LEFT, fill=Y)
s_start = Scrollbar(left)
s_start.pack(side=RIGHT, fill=Y)
s_start.config(command=t_start.yview)
t_start.config(yscrollcommand=s_start.set)
'''
t_end = Text(right, width=20)
t_end.pack(side=LEFT, fill=Y)
s_end = Scrollbar(right)
s_end.pack(side=RIGHT, fill=Y)
s_end.config(command=t_end.yview)
t_end.config(yscrollcommand=s_end.set)
'''
left.pack(side=LEFT, fill=Y)
right.pack(side=RIGHT, fill=Y)

root.geometry("500x200")
root.mainloop()