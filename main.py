from motor import Motors
from speech_recog import SpeechRecog
import time, datetime, threading, speech_recognition

print("Started At: " + str(datetime.datetime.now()))

commandTime = 1.0
speed = 100.0


sr = SpeechRecog()
motors = Motors(defSpeed=speed, defTime=commandTime)

try: 
    motors.start()
    with speech_recognition.Microphone(device_index = sr.dev_index,
                                    sample_rate = sr.sample_rate) as source:
        prev_r = "t"
        while True:
            r = sr.recog(source)
            if r is not prev_r:
                print(r)
            
            if r is None:
                pass
            elif "forward" in r:
                motors.speech_controlled = True
                motors.forward()
            elif "stop" in r:
                motors.speech_controlled = True
                motors.stop()
            elif "right" in r:
                motors.speech_controlled = True
                motors.turnRight()
            elif "l" in r:
                motors.speech_controlled = True
                motors.turnLeft()
            prev_r = r
            if motors.speech_controlled:
                time.sleep(1)
                motors.speech_controlled = False

except KeyboardInterrupt:
    motors.clean()
    motors.join()
