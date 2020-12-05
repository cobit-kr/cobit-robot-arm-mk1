from Tkinter import *
import threading 
import queue
import serial

'''
class simpleThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("simple thread init")

    def run(self):
        print("simple thread run!!!")
'''
class SerialThread(threading.Thread):

    seq = serial.Serial('/dev/cu.usbmodem14311', 9600) 
    is_run = True

    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que
    def run(self):
        while self.is_run:
            if self.seq.inWaiting():
                text = self.seq.readline(self.seq.inWaiting())
                self.queue.put(text)

class App(object):
    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print "hi!"

root = Tk()
app = App(root)
root.mainloop()