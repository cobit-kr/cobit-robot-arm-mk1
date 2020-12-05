#!/usr/bin/env python
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
        self.seq.port = '/dev/cu.usbmodem14311'
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

        serial_list = ['None']

        self.startTimer(1,False)

        tk.Tk.__init__(self)
        #self.server_running = False

        f0 = ttk.Frame(self)
        self.var = StringVar()
        f0.pack()
        self.dropdown = ttk.OptionMenu(f0, self.var, serial_list[0], *serial_list)
        self.dropdown.pack()
        self.dropdown.configure(state='normal')

        f6 = ttk.Frame(self)
        f7 = ttk.Frame(self)
        f8 = ttk.Frame(self)
        f9 = ttk.Frame(self)
      
        self.start_serial_btn = ttk.Button(f6, text="Start serial", command=self.start_serial)
        self.start_serial_btn.pack(side='left',padx=10) 
        self.stop_serial_btn = ttk.Button(f7, text="Stop serial", command=self.stop_serial)
        self.stop_serial_btn.pack(side='left',padx=10) 
        self.start_recording_btn = ttk.Button(f8, text="Start recording", command=self.start_recording)
        self.start_recording_btn.pack(side='left',padx=10) 
        self.stop_recording_btn = ttk.Button(f9, text="Stop recording", command=self.stop_recording)
        self.stop_recording_btn.pack(side='left',padx=10) 

        self.start_serial_btn.configure(state='normal')
        self.stop_serial_btn.configure(state='disable')
        self.start_recording_btn.configure(state='normal')
        self.stop_recording_btn.configure(state='disable')


        f0.grid(column=1,row=0,columnspan=3,padx=10,pady=10,sticky='w')
        f6.grid(column=1,row=1,padx=10,pady=10,sticky='w')
        f7.grid(column=2,row=1,padx=10,pady=10,sticky='w')
        f8.grid(column=1,row=2,padx=10,pady=10,sticky='w')
        f9.grid(column=2,row=2,padx=10,pady=10,sticky='w')
                                                                          
    def start_serial(self):
        print("start serial")
        self.start_serial_btn.configure(state='disable')
        self.stop_serial_btn.configure(state='normal')
        #if serial_thread.is_seq_open() == False:
        #    serial_thread.start()
        serial_thread.open_port()
        
    def stop_serial(self):
        print("stop serial")
        self.start_serial_btn.configure(state='normal')
        self.stop_serial_btn.configure(state='disable')
        serial_thread.close_port()

    def start_recording(self):
        print("start recording")
        self.start_recording_btn.configure(state='disable')
        self.stop_recording_btn.configure(state='normal')
        serial_thread.start_recording_serial()
       
    def stop_recording(self):
        print("stop recording")
        self.start_recording_btn.configure(state='normal')
        self.stop_recording_btn.configure(state='disable')
        serial_thread.stop_recording_serial()

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
    serial_thread = SerialThread()
    serial_thread.start()
    root.mainloop()