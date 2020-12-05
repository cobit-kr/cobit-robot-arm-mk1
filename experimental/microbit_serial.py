import serial
import serial.tools.list_ports as list_ports
import time


PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1


def find_comport(pid, vid, baud):
    ''' return a serial port '''
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('port: {}'.format(p))
        try:
            print('pid: {} vid: {}'.format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None


print('looking for microbit')
ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
if not ser_micro:
    print('microbit not found')
print('opening and monitoring microbit port')
ser_micro.open()
while True:
    line = ser_micro.readline().decode('utf-8')
    if line:  # If it isn't a blank line
        print(line)
    msg = "fn\n"
    ser_micro.write(msg.encode())
    time.sleep(1)
    msg = "ff\n"
    ser_micro.write(msg.encode())
    time.sleep(1)
    
ser_micro.close()