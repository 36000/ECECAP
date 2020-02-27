import speech_recognition

class SpeechRecog:
    def __init__(self):
        self.r = speech_recognition.Recognizer()

    def recog(self, source):
        self.r.listen(source)