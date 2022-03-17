serdev = '/dev/tty.usbmodem145103' # serial device of JeVois
import serial
# import time

with serial.Serial(serdev, 9600, timeout=1) as ser:
    while 1:
        line = ser.readline()
        print("Recieved: " + str(line))