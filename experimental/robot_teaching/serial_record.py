import threading 
#import tkinter as tk 
from tkinter import *
import serial 
import queue

class SerialThread(threading.Thread):

    seq = serial.Serial('/dev/cu.usbmodem14311', 9600) 
    is_run = True

    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que
    def run(self):
        while self.is_run:
            if self.seq.inWaiting():
                print("joto")
                text = self.seq.readline(self.seq.inWaiting())
                self.queue.put(text)

class Gui(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.queue = queue.Queue()
        self.thread = SerialThread(self.queue)
        self.thread.start()
        self.process_serial()

    def process_serial(self):
        while self.queue.qsize():
            try:
                received_data = self.queue.get()
                #print("Data received" + str(received_data))

                # In case, Text input field
                # self.rdata.delete(0, 'end')
                # self.rdata.insert('end', self.queue.get())

                # In case, Label
                #self.rdata.config(text=received_data)
            except queue.Empty:
                pass
        self.after(10, self.process_serial)
gui = Gui()

gui.title("Serial data recorder")
gui.mainloop()