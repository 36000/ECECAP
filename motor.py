import RPi.GPIO as GPIO
import threading
from bluetooth_wrap import BluetoothWrap
import bluetooth as bt

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

class Motors(threading.Thread):
    def __init__(self, motorPinRearLeft=32, motorPinRearRight=13, motorPinFrontLeft=12, motorPinFrontRight=33, defSpeed = 100.0, defTime = 1.0):
        GPIO.setmode(GPIO.BOARD)
        threading.Thread.__init__(self)
        self.motors = [Motor(motorPinRearLeft), Motor(motorPinRearRight), Motor(motorPinFrontLeft), Motor(motorPinFrontRight)]
        self.timer = threading.Timer(defTime, self.stop)
        self.time = defTime
        self.speed = defSpeed
        self.speech_controlled = False
    
    def run(self):
        self.bluetooth = BluetoothWrap()
        prev_r = 0
        try:
            while True:
                try:
                    r = self.bluetooth.getByte()
                    
                    if self.speech_controlled:
                        continue

                    if r != prev_r:
                        print(r, end=' ')
                    if r == b'f':
                        self.forward()
                    elif r == b's':
                        self.stop()
                    elif r == b'r':
                        self.turnRight()
                    elif r == b'l':
                        self.turnLeft()
                    prev_r = r
                
                except bt.btcommon.BluetoothError:
                    self.bluetooth.clean()
                    self.bluetooth = BluetoothWrap()

        except KeyboardInterrupt:
            self.bluetooth.clean()


    def _move(self, motors, speed, time):
        if speed == None:
            speed = self.speed
        if time == None:
            time = self.time

        self.stop()
        for motor in motors:
            motor.setSpeed(speed)

        self.timer.cancel()
        self.timer = threading.Timer(time, self.stop)
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