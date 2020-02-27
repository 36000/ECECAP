from motor import Motors
from time import sleep

commandTime = 1.0
speed = 100.0
motors = Motors(defSpeed=speed, defTime=commandTime)

try: 
    while True:
        motors.forward(50)
        sleep(0.5)

		
except:
    motors.clean()
