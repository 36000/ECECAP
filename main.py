from bluetooth_wrap import BluetoothWrap
from motor import Motors
from time import sleep
import sys

commandTime = 1.0
speed = 100.0

bluetooth = BluetoothWrap()
motors = Motors(defSpeed=speed, defTime=commandTime)

try: 
    while True:
        r = bluetooth.getChar()
        print(r)
        if r == 253:
            motors.forward()
        elif r == 255:
            motors.stop()
        elif r == 248:
            motors.turnRight()
        elif r == 254:
            motors.turnLeft()

		
except:
    motors.clean()
    bluetooth.clean()
