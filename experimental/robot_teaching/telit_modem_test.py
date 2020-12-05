import serial
import serial.tools.list_ports
import time
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
 
ports = list(serial.tools.list_ports.comports())
for p in ports: 
  print p

while 1: 
  byte5 = ser.inWaiting()
  if byte5 >0:
    str5  = ser.read(byte5) 
    print(str5)
  