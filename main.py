from bluetooth import Bluetooth
from motor import Motors
from time import sleep
import sys

if len(sys.argv) > 1:
    channel = int(sys.argv[1])
else:
    channel = 0
print("Using rfcomm" + str(channel))

commandTime = 1.0
speed = 100.0

bluetooth = Bluetooth(channel=channel)
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

		
except KeyboardInterrupt:
	motors.clean()