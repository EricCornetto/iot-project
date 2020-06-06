# ========================Virtual Assistant ===================================
#  *   Virtual Assistant Python.
# =============================================================================
#  *   Created By Eric Theodore Cornetto(Ida Bagus Dwi Putra Purnawa).
#  *   Github (https://github.com/EricCornetto).
# =============================================================================
#  *   GNU General Public License v3.0.
# =============================================================================
#             Python Artificial Intellegence
# =============================================================================

from gtts import gTTS
import speech_recognition as sr
import time
from time import ctime
import os
import webbrowser
import sys
import Adafruit_DHT
from gpiozero import *
from firebase import firebase
from datetime import datetime
import threading

firebase = firebase.FirebaseApplication("https://iot-db-bde4c.firebaseio.com/", None)
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 14
relay_lamp = OutputDevice(15)

def postData(data):
    result = firebase.post("/iot-db-bde4c/log", data)
    print(result)

def getData():
    result = firebase.get("/iot-db-bde4c/log", "")
    print(result)

def delData():
    firebase.delete("iot-db-bde4c/log", "")
    print("Record Deleted")


def postLight(data):
    result = firebase.put("/iot-db-bde4c/light","value",data)
    print(result)

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


def recordAudio():
    r = sr.Recognizer()
    os.system("sudo arecord -D plughw:1,0 --format S16_LE --rate 44100 -V mono -c1 -d 3 voice.wav")
    fileAudio = sr.AudioFile("voice.wav")
    with fileAudio as source:
        audio = r.record(source)

        data = ""
        try:
            data = r.recognize_google(audio)
            print("You Said: " + data)
        except sr.UnknownValueError:
            print("Alice Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request result from Alexa Speech Recognition Service; {0}".format(e))

        return data

def alice(data):
    if "how are you" in data:
        speak("I am fine")
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)

    if "turn on the light" in data:
        speak("Roger")
        relay_lamp.off()
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)
        postLight(True)

    if "turn off the light" in data:
        speak("Roger")
        relay_lamp.on()
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)
        postLight(False)

    if "what time is it" in data:
        speak(ctime())
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)

    if "hello Alice" in data:
        speak("Hello")
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)

    if "what is your name" in data:
        speak("My Name is Alice, iam a Virtual Assistant")
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)

    if "thank you" in data:
        speak("Your Welcome")
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)

    if "good morning" in data:
        speak("Good Morning")
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)

    if "good night" in data:
        speak("Good Night")
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)

    if "goodbye" in data:
        speak("Ok goodbye")
        recordData = {
                "Command": data,
                "Datetime": datetime.now()
                }
        postData(recordData)
        sys.exit()


def postTemp(data):
    result = firebase.put("/iot-db-bde4c/DHT22","Temperature",data)

def postHumi(data):
    result = firebase.put("/iot-db-bde4c/DHT22","Humidity", data)

time.sleep(2)
speak("Hi Master, what can I do for you?")
    
while True:
    result = firebase.get("/iot-db-bde4c/light","")
    print(result["value"])

    if result["value"] == True:
        relay_lamp.off()
    elif result["value"] == False:
        relay_lamp.on()

    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        temp = "{0:0.1f}*C".format(temperature)
        humi = "{0:0.1f}%".format(humidity)
        print(temp)
        print(humi)
        threading.Thread(target=postTemp, args=(temp,)).start()
        threading.Thread(target=postHumi, args=(humi,)).start()
    data = recordAudio()
    alice(data)
