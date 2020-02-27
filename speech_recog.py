import speech_recognition

class SpeechRecog:
    def __init__(self):
        self.r = speech_recognition.Recognizer()

    def recog(self, audio):
        self.r.recognize_google(audio)