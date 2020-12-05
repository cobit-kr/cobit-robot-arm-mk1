import serial 
import time 
import sys

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
 
#ports = list(serial.tools.list_ports.comports())
#for p in ports: 
#  print p

 
for i in range(0, 10):
    r = ser.readline()
    print(r)
    time.sleep(2)

sys.exit(0)