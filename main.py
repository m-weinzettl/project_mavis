import json
import threading
import queue
import speech_recognition as sr
import pyttsx3
import numpy as np
import pickle
import tensorflow as tf
from nltk_utils import tokenize, bag_of_words
from logic import tag_handler as th

engine = pyttsx3.init()
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 300

speech_queue = queue.Queue()

def speak(text):
    corrected_text = text.replace("Mavis", "Maiwis")
    engine.say(corrected_text)
    engine.runAndWait()

def _bg_listener_callback(rec, audio):
    try:
        text = rec.recognize_google(audio, language="de-DE")
        if text:
            speech_queue.put(text)
    except (sr.UnknownValueError, sr.RequestError):
        pass

with open('data/intents.json', 'r', encoding='utf-8') as json_file:
    intents = json.load(json_file)

with open('model/training_data.pkl', 'rb') as f:
    data = pickle.load(f)

all_words = data['all_words']
tags = data['tags']

model = tf.keras.models.load_model('model/mavis_model.keras')

def main():
    speak("Hallo ich bin Mavis. Was kann ich für dich tun.")

    print("\nMavis initialisiert Mikrofon...")
    source = sr.Microphone(device_index=1)
    stop_listening = recognizer.listen_in_background(source, _bg_listener_callback, phrase_time_limit=20)

    print("\nMavis hört zu... Befehl sprechen:")

    while True:
        sentence = speech_queue.get()

        print(f"Du hast gesagt: {sentence}")

        if "beenden" in sentence.lower():
            speak("Bis dann.")
            break

        tokenized_sentence = tokenize(sentence)
        bag = bag_of_words(tokenized_sentence, all_words)
        input_data = np.array([bag])

        output = model.predict(input_data, verbose=0)
        predicted_index = np.argmax(output)
        tag = tags[predicted_index]
        probability = output[0][predicted_index]

        print(f"Erkannte Kategorie: {tag} (Sicherheit: {probability * 100:.2f}%)")

        if probability > 0.65:
            for intent in intents['intents']:
                if tag == intent['tag']:
                    th.handle_tag(tag, intent, speak)
                    break
        else:
            speak("Das habe ich nicht verstanden. Bitte wiederholen.")

        # Löscht alles, was das Mikrofon aufgeschnappt hat, während Mavis gesprochen hat
        with speech_queue.mutex:
            speech_queue.queue.clear()

    stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    main()