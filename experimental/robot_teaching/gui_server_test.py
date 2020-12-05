#!/usr/bin/env python
import threading 
import tkinter as tk 
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
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
                text = self.seq.readline(self.seq.inWaiting())
                self.queue.put(text)

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("server thread class!")

    def create_server(self, port=8000):
        self.server = HTTPServer(("10.37.129.2", port), SimpleHTTPRequestHandler)
        self.serv_info = self.server.socket.getsockname()

    def run(self):
        self.create_server()
        self.server.serve_forever()

class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        print("GUI class")
        self.queue = queue.Queue()
        self.thread = SerialThread(self.queue)
        self.thread.start()
        self.process_serial()
    
    def process_serial(self):
        while self.queue.qsize():
            try:
                received_data = self.queue.get()
                print("Data received" + str(received_data))

                # In case, Text input field
                # self.rdata.delete(0, 'end')
                # self.rdata.insert('end', self.queue.get())

                # In case, Label
                #self.rdata.config(text=received_data)
            except queue.Empty:
                pass
        self.after(10, self.process_serial)

ser = ServerThread()
ser.start()

gui = Gui()
gui.title("GUI class")
gui.mainloop()

