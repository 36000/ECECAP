import RPi.GPIO as GPIO
from threading import Timer

from time import sleep
from enum import Enum

class MotorEnum(Enum):
    rearLeft = 0
    rearRight = 1
    frontLeft = 2
    frontRight = 3

class Motor:
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        self.pwm = GPIO.PWM(pin, 100)
        self.pwm.start(0)
        self.pin = pin

    def setSpeed(self, speed):
        self.pwm.ChangeDutyCycle(speed)
    
    def stop(self):
        self.pwm.stop()

class Motors:
    def __init__(self, motorPinRearLeft=13, motorPinRearRight=12, motorPinFrontLeft=33, motorPinFrontRight=32, defSpeed = 100.0, defTime = 1.0):
        GPIO.setmode(GPIO.BOARD)
        self.motors = [Motor(motorPinRearLeft), Motor(motorPinRearRight), Motor(motorPinFrontLeft), Motor(motorPinFrontRight)]
        self.timer = Timer(defTime, self.stop)
        self.time = defTime
        self.speed = defSpeed

    def _move(self, motors, speed, time):
        if speed == None:
            speed = self.speed
        if time == None:
            time = self.time

        self.stop()
        for motor in motors:
            motor.setSpeed(speed)

        self.timer.cancel()
        self.timer = Timer(time, self.stop)
        self.timer.start()

    def forward(self, speed=None, time=None):
        self._move(self.motors, speed, time)

    def turnLeft(self, speed=None, time=None):
        self._move(self.motors[1:5:2], speed, time)

    def turnRight(self, speed=None, time=None):
        self._move(self.motors[0:4:2], speed, time)
    
    def _testMotor(self, motor):
        self._move([motor], None, None)

    def testMotor(self, motorEnum):
        self._testMotor(self.motors[motorEnum.value])
    
    def testAllMotors(self):
        for motor in self.motors:
            self._testMotor(motor)
            sleep(self.time)
    
    def stop(self):
        for motor in self.motors:
            motor.setSpeed(0)

    def clean(self):
        GPIO.cleanup()

        GPIO.setmode(GPIO.BOARD)
        for motor in self.motors:
            GPIO.setup(motor.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)