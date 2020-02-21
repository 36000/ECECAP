from motor import Motors

motors = Motors()

try: 
	while True:
		motors.testAllMotors()

except KeyboardInterrupt:
	motors.clean()