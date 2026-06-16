import json
import os
import speech_recognition as sr
import numpy as np
import pickle
import tensorflow as tf
from gtts import gTTS
import pygame
from nltk_utils import tokenize, bag_of_words
from logic import tag_handler as th

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 300


def speak(text):
    corrected_text = text.replace("Mavis", "Mavis")
    tts = gTTS(text=corrected_text, lang='de')
    filename = "voice.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    pygame.mixer.quit()

    try:
        os.remove(filename)
    except OSError:
        pass


def listen(source):
    print("\nMavis hört zu... Befehl sprechen:")
    try:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        return recognizer.recognize_google(audio, language="de-DE")
    except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
        return ""


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
    with sr.Microphone(device_index=1) as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            sentence = listen(source)

            if sentence == "":
                continue

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


if __name__ == "__main__":
    main()