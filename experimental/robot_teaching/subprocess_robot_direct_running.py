import serial
import time 
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--serial", type=str, help="select serial port")

args = vars(parser.parse_args())

if not args.get("serial", False):
    print("Select serial port")
    sys.exit(1)

seq = serial.Serial(args["serial"], 9600)

while True:
    # move some point 
    seq.write("4a115b103c107d136e37f129g\n")
    time.sleep(3)
    byte1 = seq.inWaiting()
    str1 = seq.read(byte1)
    print(str1)
    # home
    seq.write("3\n")
    time.sleep(3)
    byte2 = seq.inWaiting()
    str2 = seq.read(byte2)
    print(str2)