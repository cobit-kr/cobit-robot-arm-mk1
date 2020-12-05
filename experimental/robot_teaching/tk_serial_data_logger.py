#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
#import socket
from threading import Thread, Event
import serial
import glob
import time
import sys 
import threading

#Python 2.7 imports
try:
    import Tkinter as tk
    from Tkinter import StringVar
    import ttk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    import Queue
    import commands
#Python 3.x imports
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import filedialog
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
            timeout=1
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
            if self.fuckyou == True:
                print("Serial run")
                time.sleep(1)
            elif self.fuckyou == False:
                print("Serial close")
                time.sleep(1)
            if self.seq.isOpen() == True:  
                print("Thread run")
                if self.seq.inWaiting():
                    text = self.seq.readline(self.seq.inWaiting())
                    print(text)    
                    if self.recording_flag == True: 
                        self.filename.write(text) 

    def open_port(self):
        self.fuckyou = True
        if self.seq.isOpen() == False:
            self.seq.open()

    def close_port(self):
        if self.seq.isOpen() == True:
            self.seq.close()
        self.seq.close()       
        self.fuckyou = False

    def start_recording_serial(self):
        print("start serial recording")
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.filename = open(self.timestr+".txt",'w')
        self.recording_flag = True

    def stop_recording_serial(self):
        print("stop serial recording")
        self.filename.close()
        self.recording_flag = False

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
        
        f1 = ttk.Frame(self)
        f2 = ttk.Frame(self)
        f3 = ttk.Frame(self)  # link 0  
        f4 = ttk.Frame(self)  # link 1
        f5 = ttk.Frame(self)  # link 2
        f6 = ttk.Frame(self)  # button: save
       
      
        self.start_serial_btn = ttk.Button(f1, text="Start serial", command=self.start_serial)
        self.start_serial_btn.pack(side='left',padx=10) 
        self.stop_serial_btn = ttk.Button(f2, text="Stop serial", command=self.stop_serial)
        self.stop_serial_btn.pack(side='left',padx=10) 

        self.start_serial_btn.configure(state='disable')
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
       
    def OptionMenu_Selected(self, value): 
        print(value)

    def OptionMenu_Changed(self, *args): 
        print(self.var.get())
        serial_thread.get_serial_port(self.var.get())
        self.start_serial_btn.configure(state='enable')
        self.start_recording_btn.configure(state='enable')

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
    root = Gui()
    serial_queue = Queue.Queue()
    serial_thread = SerialThread()
    root.mainloop()