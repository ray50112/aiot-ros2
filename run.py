import serial
import time

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)
i=1
while True:
    
    if(i<3):
        port.write('B'.encode('ascii'))
        time.sleep(1)

        port.write('R'.encode('ascii'))
        time.sleep(1)

        port.write('L'.encode('ascii'))
        time.sleep(1)

        port.write('F'.encode('ascii'))
        time.sleep(1)
        
    i+=1

