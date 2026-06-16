import speech_recognition as sr
import pyttsx3
import os

engine = pyttsx3.init()

def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    print("\n--- Verfügbare Audio-Geräte ---")
    for index, name in enumerate(mic_list):
        # Konvertiert den Namen sauber in UTF-8, um Windows-Umlautfehler abzufangen
        safe_name = name.encode('utf-8', errors='ignore').decode('utf-8')
        print(f"Index {index}: {safe_name}")
    print("--------------------------------\n")

def speak(text):
    korrigierter_text = text.replace("Mavis", "Maiwis")
    engine.say(korrigierter_text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 300

    # Wir übergeben hier explizit dein Arctis Nova 3 Headset (Index 1)
    with sr.Microphone(device_index=1) as source:
        print("Mavis kalibriert dein Headset... Bitte kurz ruhig sein.")
        recognizer.adjust_for_ambient_noise(source, duration=2)

        print("\n=== JETZT ÜBER HEADSET SPRECHEN! ===")
        audio = recognizer.listen(source, timeout=120, phrase_time_limit=120)

    try:
        print("Mavis verarbeitet die Audio-Daten...")
        text = recognizer.recognize_google(audio, language="de-DE")
        return text
    except sr.UnknownValueError:
        return "Entschuldigung, das habe ich nicht verstanden."
    except sr.RequestError:
        return "Fehler: Verbindung zum Erkennungsdienst fehlgeschlagen."
