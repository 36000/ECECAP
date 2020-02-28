from bluetooth_wrap import BluetoothWrap
from motor import Motors
from speech_recog import SpeechRecog
from time import sleep
import sys

t_audio = True

commandTime = 1.0
speed = 100.0

bluetooth = BluetoothWrap()
sr = SpeechRecog()
motors = Motors(defSpeed=speed, defTime=commandTime)

try: 
    prev_r = 0
    while True:
        if t_audio:
            r = bluetooth.getAudio()
            print(r)
            sr.play(r)
            q = sr.recog(r)
            print(q)
            sleep(2.0)
        else:
            r = bluetooth.getChar()
            if r != prev_r:
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
    bluetooth.clean()
