import json
import speech_recognition as sr
import pyttsx3
import numpy as np
import pickle
import tensorflow as tf
from nltk_utils import tokenize, bag_of_words
from logic import tag_handler as th

engine = pyttsx3.init()

def speak(text):
    corrected_text = text.replace("Mavis", "Maiwis")
    engine.say(corrected_text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 300

    with sr.Microphone(device_index=1) as source:
        print("\nMavis hört zu... Befehl sprechen:")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=120, phrase_time_limit=20)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio, language="de-DE")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

# 1. Daten und gelernte Strukturen laden
with open('data/intents.json', 'r', encoding='utf-8') as json_file:
    intents = json.load(json_file)

with open('model/training_data.pkl', 'rb') as f:
    data = pickle.load(f)

all_words = data['all_words']
tags = data['tags']

model = tf.keras.models.load_model('model/mavis_model.keras')

if __name__ == "__main__":
    speak("Hallo ich bin Mavis. Was kann ich für dich tun.")

    while True:
        sentence = listen()

        if sentence == "":
            print("Keine Sprache erkannt, starte neuen Versuch...")
            continue

        print(f"Du hast gesagt: {sentence}")

        if "beenden" in sentence.lower():
            speak("Bis dann.")
            break

        # Text für das Modell vorbereiten
        tokenized_sentence = tokenize(sentence)
        bag = bag_of_words(tokenized_sentence, all_words)

        # Das Modell erwartet eine Matrix (zweidimensionales Array)
        input_data = np.array([bag])

        # Vorhersage des Modells berechnen
        output = model.predict(input_data, verbose=0)
        predicted_index = np.argmax(output)
        tag = tags[predicted_index]

        # Wahrscheinlichkeit direkt aus der Ausgabe extrahieren
        probability = output[0][predicted_index]

        print(f"Erkannte Kategorie: {tag} (Sicherheit: {probability * 100:.2f}%)")

        # Wenn die Sicherheit über siebzig Prozent liegt, wird die Aktion ausgeführt
        if probability > 0.7:
            for intent in intents['intents']:
                if tag == intent['tag']:
                    th.handle_tag(tag, intent, speak)
        else:
            speak("Das habe ich nicht verstanden. Bitte wiederholen.")