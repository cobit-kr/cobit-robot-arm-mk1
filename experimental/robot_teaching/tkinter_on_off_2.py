from Tkinter import *
from threading import Thread, Event
import queue
import serial
import time
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

class ServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("server thread class!")

    def create_server(self, port=8000):
        self.server = HTTPServer(("10.37.129.2", port), SimpleHTTPRequestHandler)
        self.serv_info = self.server.socket.getsockname()

    def run(self):
        print("ssibal")
        self.create_server()
        self.server.serve_forever()

    def stop(self):
        print("zotto")
        self.server.shutdown()
        self.server.server_close()
       
    


class Controller(object):
    
    seq = serial.Serial('/dev/cu.usbmodem14311', 9600) 
    
    def __init__(self):
        self.thread = None
        self.queue = queue.Queue()
        self.stop_threads = Event()

    def loop(self):
        while not self.stop_threads.is_set():
            if self.seq.inWaiting(): 
                text = self.seq.readline(self.seq.inWaiting())
                self.queue.put(text)
                print(text)  
                  
    def combine(self):
        self.stop_threads.clear()
        self.thread = Thread(target = self.loop)   
        self.thread.start()
        print("combine")

    def stop(self):
        self.stop_threads.set()
        try:
            self.thread.join()
        except:
            pass
        self.thread = None
        print("stop")

def _delete_window():
    print("delete_window")
    ser.stop()
    ser.join()
    control.stop()
    try:
        root.destroy()
    except:
        pass

def _destroy(event):
    print("destroy")


ser = ServerThread()
ser.start()
root = Tk()

root.protocol("WM_DELETE_WINDOW", _delete_window)
root.bind("<Destroy>", _destroy)

mainframe = Frame(root)
control = Controller()
btn1 = Button(root, text="Start Recording", width=16, height=5, command=control.combine)
btn1.grid(row=2,column=0)
btn2 = Button(root, text="Stop Recording", width=16, height=5, command=control.stop)
btn2.grid(row=3,column=0)
root.mainloop()