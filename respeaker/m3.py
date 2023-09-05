from tuning import Tuning
import usb.core
import usb.util
import time
import serial

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

if dev:
    Mic_tuning = Tuning(dev)
    print(Mic_tuning.direction)
    while True:
        try:
            direction = Mic_tuning.direction
            print(f"声音方向: {direction} 度")
            if(direction<15): ##右
                port.write('D'.encode('ascii'))
                time.sleep(3)
            elif(direction<45): ##右右前
                port.write('E'.encode('ascii'))
                time.sleep(3)
            elif(direction<75): ##前右前
                port.write('R'.encode('ascii'))
                time.sleep(3)
            elif(direction<105): ##前
                port.write('W'.encode('ascii'))
                time.sleep(3)
            elif(direction<135): ##左前前
                port.write('Q'.encode('ascii'))
                time.sleep(3)
            elif(direction<165): ##左左前
                port.write('T'.encode('ascii'))
                time.sleep(3)
            elif(direction<195): ##左
                port.write('A'.encode('ascii'))
                time.sleep(3)
            elif(direction<225): ##左左後
                port.write('Z'.encode('ascii'))
                time.sleep(3)
            elif(direction<255): ##後左後
                port.write('B'.encode('ascii'))
                time.sleep(3)
            elif(direction<285): ##後
                port.write('S'.encode('ascii'))
                time.sleep(3)
            elif(direction<315): ##後右後
                port.write('C'.encode('ascii'))
                time.sleep(3)
            elif(direction<345): ##右右後
                port.write('V'.encode('ascii'))
                time.sleep(3)
            elif(direction>=345): ##右
                port.write('D'.encode('ascii'))
                time.sleep(3)
        except KeyboardInterrupt:
            break