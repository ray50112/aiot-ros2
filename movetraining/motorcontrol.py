import cv2
import serial

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)

lastCmd = ''

while 1:
    key = ''
    ret,frame = cap.read()
    commandList= {ord('w'):'1_50\n',
                  ord('s'):'4_50\n',
                  ord('a'):'3_50\n',
                  ord('d'):'2_50\n'}
    key = cv2.waitKey(50) & 0xff
    
    if key == ord('q'):
        ser.write('8_50\n'.encode())
        cv2.destroyAllWindows()
        cap.release()
        break
    elif key in commandList:
        lastCmd = key
        ser.write(commandList[key].encode())
        print(key)
    else:
        pass

    if lastCmd == ord('w'):
        cv2.putText(frame,'W',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3,cv2.LINE_AA)
    else:
        cv2.putText(frame,'W',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),3,cv2.LINE_AA)

    if lastCmd == ord('s'):
        cv2.putText(frame,'S',(50,80),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3,cv2.LINE_AA)
    else:
        cv2.putText(frame,'S',(50,80),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),3,cv2.LINE_AA)

    if lastCmd == ord('a'):
        cv2.putText(frame,'A',(30,80),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3,cv2.LINE_AA)
    else:
        cv2.putText(frame,'A',(30,80),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),3,cv2.LINE_AA)

    if lastCmd == ord('d'):
        cv2.putText(frame,'D',(70,80),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3,cv2.LINE_AA)
    else:
        cv2.putText(frame,'D',(70,80),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),3,cv2.LINE_AA)

    cv2.imshow('frame',frame)

