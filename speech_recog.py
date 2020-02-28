import speech_recognition as sr
import simpleaudio as sa

class SpeechRecog:
    def __init__(self):
        self.r = sr.Recognizer()

        self.sample_rate = 32000
        self.sample_width = 2
        self.test_sample = b"T\xb5M\xaddKT\xad.\xd5MM\x92S5\xd9MUUU6\x8dSU\x93\x95Me\x8b\x96M\x995\xa9ee\x95\x95\x95VUf\x95fiefeU\x99i\xa6\x99VV\x9affj\xa5\xa5e\xa5\xa9Z\xa9\x95\xa9\x95\xb2W\xaa\xa6)\xaa\xa5\xa6\x9a\xc9\xa5\xa6\xaa"

    def recog(self, audio):
        try:
            result = self.r.recognize_google(sr.AudioData(audio, self.sample_rate, self.sample_width))
        except sr.UnknownValueError:
            result = None
        return result
    
    def play(self, audio):
        play_obj = sa.play_buffer(audio, 1, self.sample_width, self.sample_rate)
        play_obj.wait_done()

