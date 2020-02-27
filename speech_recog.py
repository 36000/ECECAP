import speech_recognition as sr

class SpeechRecog:
    def __init__(self):
        self.r = sr.Recognizer()

    def recog(self, audio):
        sample_rate = 32000
        sample_width = 2
        try:
            result = self.r.recognize_google(sr.AudioData(audio, sample_rate, sample_width))
        except sr.UnknownValueError:
            result = None
        return result