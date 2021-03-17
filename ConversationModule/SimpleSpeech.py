import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init() 

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

from os import path
AUDIO_FILE = "TestVoice.wav"

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

try:
    s = r.recognize_google(audio)
    print("I think you said : " + s)
    engine.save_to_file(s, 'result.mp3')
    engine.runAndWait()
except sr.UnknownValueError:
    print("I could not understand audio")
except sr.RequestError as e:
    print("Error; {0}".format(e))


