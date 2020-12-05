#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
#from socket import *
from threading import Thread, Event
import serial
import glob
import time
import sys 
import threading
import socket

#Python 2.7 imports
try:
    import Tkinter as tk
    from Tkinter import StringVar
    import ttk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    #from SimpleHTTPServer import SimpleHTTPRequestHandler
    import SimpleHTTPServer
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

class SerialThread(Thread):

    #self.seq = serial.Serial('/dev/cu.usbmodem14311', 9600) 
    def __init__(self):
        Thread.__init__(self)

        self.recording_flag = False
        
        self.seq = serial.Serial(
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None
        )
        #self.seq.port = '/dev/cu.usbmodem14311'
        self.seq.port = "None"
        #if self.seq.isOpen() != True:
        #    self.seq.open()
        #self.seq.open()
        self.queue = serial_queue
        self.is_serial_running = False
        self.daemon = True
        self.fuckyou = True

    def run(self):
        while True:
            #if self.fuckyou == True:
                #print("Serial run")
                #time.sleep(1)
            #elif self.fuckyou == False:
                #print("Serial close")
                #time.sleep(1)
            time.sleep(0.1)
            if self.seq.isOpen() == True:  
                #print("Thread run")
                num = self.seq.inWaiting()
                if num > 0:
                    text = self.seq.read(num)
                    print(text)    
                    #if self.recording_flag == True: 
                    #    self.filename.write(text) 

    def open_port(self):
        self.fuckyou = True
        if self.seq.isOpen() == False:
            self.seq.open()

    def close_port(self):
        if self.seq.isOpen() == True:
            self.seq.close()
        self.seq.close()       
        self.fuckyou = False

    def is_seq_open(self):
        if self.seq.isOpen() == True:
            return True
        else:
            return False

    def get_serial_port(self, port_name):
        self.seq.port = port_name

    def serial_ports(self):   
        if sys.platform.startswith('win'):   
            self.ports = ['COM%s' % (i + 1) for i in range(256)]   
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):   
            # this excludes your current terminal "/dev/tty"   
            self.ports = glob.glob('/dev/tty[A-Za-z]*')   
        elif sys.platform.startswith('darwin'):   
            self.ports = glob.glob('/dev/tty.*')   
        else:   
            raise EnvironmentError('Unsupported platform')   
        
        self.result = []   
        for self.port in self.ports:   
            try:   
                self.s = serial.Serial(self.port)   
                self.s.close()   
                self.result.append(self.port)   
            except (OSError, serial.SerialException):   
                pass   
        return self.result   

class ServerThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.queue = server_queue
        self.is_server_running = False 
        self.daemon = True
        self.server = HTTPServer(("127.0.0.1", 8081), Handler)
        self.serv_info = self.server.socket.getsockname()
        print(self.serv_info)

       
    #def create_server(self, port=8000):
        #self.server = HTTPServer((ip_address, port), SimpleHTTPRequestHandler)
        #self.server = HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler)
        #self.serv_info = self.server.socket.getsockname()


    def run(self):
        self.server.serve_forever()

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        """Send response headers"""
        if self.path != "/":
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_HEAD(self)
        self.send_response(200)
        self.send_header("content-type", "text/html;charset=utf-8")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        """Send page text"""
        if self.path != "/":
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.send_response(302)
            #self.send_header("Location", "/blockly/demos/code/index.html")
            self.send_header("Location", "/blockly/apps/cobit_blockly/index.html")
            self.end_headers()

    def do_POST(self):
        """Save new page text and display it"""
        if self.path != "/":
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_POST(self)

        #options, args = parser.parse_args()

        length = int(self.headers.getheader('content-length'))
        if length:
            text = self.rfile.read(length)
                        
            print "sketch to upload: " + text

            dirname = tempfile.mkdtemp()
            sketchname = os.path.join(dirname, os.path.basename(dirname)) + ".py"
            f = open(sketchname, "wb")
            f.write(text + "\n")
            f.close()

            print "created sketch at %s" % (sketchname,)
            # invoke arduino to build/upload
            compile_args = [
                'python',
                 sketchname,
            ]

            #compile_args.append(sketchname)

            print "Uploading with %s" % (" ".join(compile_args))
            rc = subprocess.call(compile_args)

            if not rc == 0:
                print "python returned " + `rc`                            
                self.send_response(400)
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
        else:
            self.send_response(400)

class SocketThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        HOST,PORT = '127.0.0.1',8082 # host -> socket.gethostname() use to set machine IP  
        self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.my_socket.bind((HOST,PORT))
        self.my_socket.listen(1)
        

    def run(self):
        while True:
            self.connection,self.address = self.my_socket.accept()
            self.request = self.connection.recv(1024).decode('utf-8')
            self.connection.sendall('test')
            print(self.request)
            #self.connection.close()

'''
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
'''        
class Gui(tk.Tk):

    def __init__(self):

        serial_list = ['시리얼 포트를 선택하세요.']

        self.startTimer(1,False)

        tk.Tk.__init__(self)
        self.serial_running = False

        f0 = ttk.Frame(self)
        self.var = StringVar()
        f0.pack()
        self.dropdown = ttk.OptionMenu(f0, self.var, serial_list[0], *serial_list, command = self.OptionMenu_Selected(self.var))
        self.dropdown.pack()
        self.dropdown.configure(state='normal')

        self.var.trace('w', self.OptionMenu_Changed)
        
        f1 = ttk.Frame(self)  # button: start serial
        f2 = ttk.Frame(self)  # button: stop serial 
        f3 = ttk.Frame(self)  # link 0  
        f4 = ttk.Frame(self)  # link 1
        f5 = ttk.Frame(self)  # link 2
        f6 = ttk.Frame(self)  # button: save
        #f7 = ttk.Frame(self)  #  
        #f8 = ttk.Frame(self)  # 
        
        # start serial button 
        self.start_serial_btn = ttk.Button(f1, text="Start serial", command=self.start_serial)
        self.start_serial_btn.pack(side='left',padx=10) 
        self.start_serial_btn.configure(state='disable')
        # stop serial button
        self.stop_serial_btn = ttk.Button(f2, text="Stop serial", command=self.stop_serial)
        self.stop_serial_btn.pack(side='left',padx=10) 
        self.stop_serial_btn.configure(state='disable')
        #Link 0 
        ttk.Label(f3,text='Link 0: ',font='Helvetica 10 bold').pack(side='left')
        self.port = ttk.Entry(f3,width=6)
        self.port.insert('end','80')
        self.port.pack(side='left',padx=0,pady=10)
        #Link 1 
        ttk.Label(f4,text='Link 1: ',font='Helvetica 10 bold').pack(side='left')
        self.port = ttk.Entry(f4,width=6)
        self.port.insert('end','80')
        self.port.pack(side='left',padx=0,pady=10)
        #lin 3
        ttk.Label(f5,text='Link 2: ',font='Helvetica 10 bold').pack(side='left')
        self.port = ttk.Entry(f5,width=6)
        self.port.insert('end','80')
        self.port.pack(side='left',padx=0,pady=10)
        # save btn
        self.save_link_btn = ttk.Button(f6, text="save link", command=self.save_link)
        self.save_link_btn.pack(side='left',padx=10) 
        

        f0.grid(column=1,row=0,columnspan=3,padx=10,pady=10,sticky='w')
        f1.grid(column=1,row=1,padx=10,pady=10,sticky='w')
        f2.grid(column=2,row=1,padx=10,pady=10,sticky='w')
        f3.grid(column=1,row=2,padx=10,pady=10,sticky='w')
        f4.grid(column=2,row=2,padx=10,pady=10,sticky='w')
        f5.grid(column=3,row=2,padx=10,pady=10,sticky='w')
        f6.grid(column=4,row=2,padx=10,pady=10,sticky='w')
        #f7.grid(column=5,row=2,padx=10,pady=10,sticky='w')
        #f8.grid(column=6,row=2,padx=10,pady=10,sticky='w')


    def OptionMenu_Selected(self, value): 
        print(value)

    def OptionMenu_Changed(self, *args): 
        print(self.var.get())
        serial_thread.get_serial_port(self.var.get())
        self.start_serial_btn.configure(state='enable')

    def save_link(self):
        print("save link")
                                                                  
    def start_serial(self):
        print("start serial")
        self.start_serial_btn.configure(state='disable')
        self.stop_serial_btn.configure(state='normal')
        if self.serial_running == False:
            self.serial_running = True
            serial_thread.start()   
        serial_thread.open_port()
        
    def stop_serial(self):
        print("stop serial")
        self.start_serial_btn.configure(state='normal')
        self.stop_serial_btn.configure(state='disable')
        serial_thread.close_port()

    def timerCallBack(self, iTimeSec,isRepeated):
        self.result = serial_thread.serial_ports()
        self.serial_list = self.result
        print(self.serial_list)
        self.update_option_menu()
        self.dropdown.configure(state='enable')
       
        if isRepeated == True :
            threading.Timer(iTimeSec,timerCallBack,[iTimeSec,isRepeated]).start()

    def startTimer(self, iTimeSec,isRepeated):
        threading.Timer(iTimeSec,self.timerCallBack,[iTimeSec,isRepeated]).start()

    def update_option_menu(self):
        self.menu = self.dropdown["menu"]
        self.menu.delete(0, "end")
        for string in self.serial_list:
            self.menu.add_command(label=string, command=lambda value=string: self.var.set(value))

          
if __name__ == '__main__':

    #ports = glob.glob('/dev/cu*')
    #for port in ports:
    #    print port
    
    root = Gui()
    serial_queue = Queue.Queue()
    server_queue = Queue.Queue()
    serial_thread = SerialThread()
    server_thread = ServerThread()
    server_thread.start()
    socket_thread = SocketThread()
    socket_thread.start()
    #serial_thread.start()
    root.mainloop()