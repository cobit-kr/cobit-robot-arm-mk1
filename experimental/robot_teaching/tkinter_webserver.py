#!/usr/bin/env python
import os
import socket
from threading import Thread, Event
import serial
import glob
import time


#Python 2.7 imports
try:
    import Tkinter as tk
    from Tkinter import StringVar
    import ttk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
    import Queue
    import commands
#Python 3.x imports
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import filedialog
    from http.server import SimpleHTTPRequestHandler
    from http.server import HTTPServer
    import queue as Queue
    import subprocess as commands



class ServerThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.queue = server_queue
        self.is_server_running = False 
        self.daemon = True

       
    def create_server(self, port=8000):
        #self.server = HTTPServer((ip_address, port), SimpleHTTPRequestHandler)
        self.server = HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler)
        self.serv_info = self.server.socket.getsockname()


    def run(self):
        while True:
            if not self.queue.empty():
                i = self.queue.get()
                if i[0] == 'start':
                    print("ssibal")
                    self.create_server(int(i[1]))
                    self.is_server_running = True
                    print('SERVING @: {}:{}'.format(self.serv_info[0],self.serv_info[1]))
                    self.server.serve_forever()
                elif i[0] == 'stop':
                    self.is_server_running=False
                    print('SERVER SHUTDOWN')
                    self.server = None
                    print("jotto")
            

class SerialThread(Thread):

    #seq = serial.Serial('/dev/cu.Bluetooth-Incoming-Port', 9600) 
    

    def __init__(self):
        Thread.__init__(self)
        self.seq = serial.Serial(
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.seq.port = '/dev/cu.Bluetooth-Incoming-Port'
        self.queue = serial_queue
        self.is_serial_running = False
        self.daemon = True
        self.fuckyou = False

    def run(self):
        while True:
            if self.fuckyou == True:
                print("fuck you")
                time.sleep(1)
            elif self.fuckyou == False:
                print("siva joto")
                time.sleep(1)
            #if self.seq.inWaiting():
            #    text = self.seq.readline(self.seq.inWaiting())
                #self.queue.put(text)
            #    print(text)     

    def open_port(self):
        self.fuckyou = True
        self.seq.open()

    def close_port(self):
        self.seq.close()       
        self.fuckyou = False
            
        
class Gui(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.server_running = False

        f0 = ttk.Frame(self)   
        f1 = ttk.Frame(self)
        f2 = ttk.Frame(self)
        f3 = ttk.Frame(self)
        f4 = ttk.Frame(self)
        f5 = ttk.Frame(self)

        f6 = ttk.Frame(self)
        f7 = ttk.Frame(self)

        ttk.Label(f0,text='Port can be 1-65535. A blank directory path will host the directory\nthat contains this program').pack(side='left')
        ttk.Label(f1,text='Your IP address:  {}'.format(ip_address),font='Helvetica 10 bold').pack()
        ttk.Label(f2,text='Port to host on: ',font='Helvetica 10 bold').pack(side='left')
        self.port = ttk.Entry(f2,width=6)
        self.port.insert('end','8000')
        self.port.pack(side='left',padx=0,pady=10)
        ttk.Label(f3,text='Directory to host: ',font='Helvetica 10 bold').pack(side='left')
        self.path_entry = ttk.Entry(f3,width=70)
        self.path_entry.insert('end',OWD)
        self.path_entry.pack(side='left')
        ttk.Button(f3,text='Browse',command=self.browse).pack(side='left',padx=10)
        ttk.Label(f4,text='Start/Stop the server: ',font='Helvetica 10 bold').pack(side='left')
        self.start_btn = ttk.Button(f4,text='Start server',command=self.start_clicked)
        self.start_btn.pack(side='left',padx=10)
        self.stop_btn = ttk.Button(f4,text='Stop server',command=self.stop_clicked,state='disabled')
        self.stop_btn.pack(side='left',padx=10)
        ttk.Label(f5,text='Server state: ',font='Helvetica 10 bold').pack(side='left')
        self.serverstate_lbl = ttk.Label(f5,text='Stopped',font='Helvetica 15 bold',foreground='red')
        self.serverstate_lbl.pack(side='left')
        
        self.start_serial_btn = ttk.Button(f6, text="Start serial", command=self.start_serial)
        self.start_serial_btn.pack(side='left',padx=10) 
        self.stop_serial_btn = ttk.Button(f6, text="Stop serial", command=self.stop_serial)
        self.stop_serial_btn.pack(side='left',padx=10) 


        f0.grid(column=1,row=0,columnspan=3,padx=10,pady=10,sticky='w')
        f1.grid(column=1,row=1,padx=10,pady=10,sticky='w')
        f2.grid(column=1,row=2,padx=10,pady=10,sticky='w')
        f3.grid(column=1,row=3,columnspan=3,padx=10,pady=10,sticky='w')
        f4.grid(column=1,row=4,padx=10,pady=10,sticky='w')
        f5.grid(column=2,row=4,padx=10,pady=10,sticky='w')
        f6.grid(column=1,row=5,padx=10,pady=10,sticky='w')
        f7.grid(column=2,row=5,padx=10,pady=10,sticky='w')
                                                                          
    def browse(self):
        path = filedialog.askdirectory()
        if os.path.isdir(path):
            self.path_entry.delete('0',tk.END)
            self.path_entry.insert('end',path)

    def start_clicked(self): 
        #if server_thread.is_server_running:
            #messagebox.showerror('Already running','The server is already running. Please stop the server first!')
            #return
        if switch_dir(self.path_entry.get()):
            port = check_port(self.port.get().strip())
            if not port:
                messagebox.showerror('Error','Please enter a valid port number between 1-65535')
                return
            server_queue.put(('start',port))

            # wait for the server_thread to switch is_server_running = True
            while not server_thread.is_server_running:
                pass
            self.toggle_state_widgets()
            messagebox.showinfo('NOW SERVING','Now serving {} @{}:{}'.format(os.getcwd(),ip_address,port))
        else:
            messagebox.showerror('Invalid path','The path you have provided does not exist!')
        
    def stop_clicked(self,notify=True):
        if server_thread.is_server_running:
            server_queue.put(('stop',''))
            server_thread.server.shutdown()
            
            # wait for the server thread to switch isruuning = False
            while server_thread.is_server_running:
                pass
            self.toggle_state_widgets()
            if notify: 
                messagebox.showinfo('SERVER SHUTDOWN', 'The server has been shutdown.')

    def toggle_state_widgets(self):
        if server_thread.is_server_running:
            self.start_btn.configure(state='disabled')
            self.stop_btn.configure(state='normal')
            txt = 'Serving'
            color = 'green'
        else:
            self.start_btn.configure(state='normal')
            self.stop_btn.configure(state='disabled')
            txt = 'Stopped'
            color = 'red'
        self.serverstate_lbl.configure(text=txt,foreground=color)

    def start_serial(self):
        print("start serial")
        serial_thread.open_port()

    def stop_serial(self):
        print("stop serial")
        serial_thread.close_port()
        
        
def get_ip_address():
    if os.name == 'posix':
        ip = commands.getoutput("hostname -I")
    elif os.name == 'nt':
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = ''
        print('Couldn\'t get local ip')
    return ip

def switch_dir(path):
    if os.path.isdir(path):
        os.chdir(path)
        return True
    if path == '':
        os.chdir(OWD)
        return True
    else:
        return

def check_port(port):
    try:
        p = int(port)
        if p > 65535:
            return
        else:
            return p
    except Exception as e:
        print(e)
        return
    

          
if __name__ == '__main__':

    ports = glob.glob('/dev/cu*')
    for port in ports:
        print port

    OWD = os.getcwd()
    ip_address = get_ip_address()
    root = Gui()
    server_queue = Queue.Queue()
    serial_queue = Queue.Queue()
    server_thread = ServerThread()
    serial_thread = SerialThread()
    server_thread.start()
    serial_thread.start()
    root.mainloop()