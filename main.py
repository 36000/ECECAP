from bluetooth_wrap import BluetoothWrap
from motor import Motors
from speech_recog import SpeechRecog
from time import sleep
import sys, datetime

print("Started At: " + str(datetime.datetime.now()))

commandTime = 1.0
speed = 100.0

bluetooth = BluetoothWrap()
sr = SpeechRecog()
motors = Motors(defSpeed=speed, defTime=commandTime)

try: 
    prev_r = 0
    while True:
        r = bluetooth.getByte()
        
        if r != prev_r:
            print(r, end=' ')
        if r == b'f':
            motors.forward()
        elif r == b's':
            motors.stop()
        elif r == b'r':
            motors.turnRight()
        elif r == b'l':
            motors.turnLeft()

		
except KeyboardInterrupt:
    motors.clean()
    bluetooth.clean()
