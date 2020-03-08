import speech_recognition as sr
import pyaudio as pa

class SpeechRecog:
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.energy_threshold = 200
        #self.r.dynamic_energy_threshold = False

        self.sample_rate = 44100

        self.dev_index = None
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if "Audio" in microphone_name:
                self.print("Audio Device Found: " + microphone_name)
                self.dev_index = i

        if self.dev_index is None:
            self.print("Error: No Device Found")

    def recog(self, mic):
        try:
            return self.r.recognize_google(self.r.listen(mic,
                                                         phrase_time_limit=3),
                                        #    keyword_entries=[
                                        #        ("right", 1.0),
                                        #        ("left", 1.0),
                                        #        ("stop", 1.0),
                                        #        ("forward", 1.0),
                                        #    ],
                                           language='en-US',
                                           show_all=False)
        except sr.UnknownValueError:
            return None

    def print(self, string):
        print('Speech-Module: ' + string)

