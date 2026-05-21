import json
import random
import os
import speech_recognition as sr
import pyttsx3
import numpy as np
import pickle
import tensorflow as tf
from nltk_utils import tokenize, stem, bag_of_words

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 300

    with sr.Microphone(device_index=1) as source:
        print("\nMavis hört zu... Befehl sprechen:")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        text = recognizer.recognize_google(audio, language="de-DE")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""


# 1. Daten und gelernte Strukturen laden
# Hier wurde der Tippfehler im Dateinamen korrigiert (intents statt intetns)
with open('data/intents.json', 'r', encoding='utf-8') as json_file:
    intents = json.load(json_file)

# Hier wurde der Ordnerpfad korrigiert (model statt models)
with open('model/training_data.pkl', 'rb') as f:
    data = pickle.load(f)

all_words = data['all_words']
tags = data['tags']

# Hier wurde das moderne Dateiformat eingetragen, das wir beim Training gespeichert haben
model = tf.keras.models.load_model('model/mavis_model.keras')

if __name__ == "__main__":
    speak("System online. Ich höre.")

    sentence = listen()
    if sentence != "":
        print(f"Du hast gesagt: {sentence}")

        # Text für das Modell vorbereiten
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)

        # Das Modell erwartet eine Matrix (zweidimensionales Array), kein einfaches Array
        X = np.array([X])

        # Vorhersage des Modells berechnen
        output = model.predict(X, verbose=0)
        predicted_index = np.argmax(output)
        tag = tags[predicted_index]

        # Wahrscheinlichkeit für die gefundene Kategorie berechnen
        probabilities = tf.nn.softmax(output)
        probability = probabilities[0][predicted_index].numpy()

        # Wenn die Sicherheit über siebzig Prozent liegt, wird die Aktion ausgeführt
        if probability > 0.7:
            for intent in intents['intents']:
                if tag == intent['tag']:
                    if tag == "open_notepad":
                        speak(random.choice(intent['responses']))
                        os.system("notepad.exe")
                    else:
                        speak(random.choice(intent['responses']))
        else:
            speak("Das habe ich nicht verstanden. Bitte wiederholen.")
    else:
        speak("Ich habe dich nicht gehört.")