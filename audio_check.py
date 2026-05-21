import speech_recognition as sr
import pyttsx3
import os

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
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
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        print("Mavis verarbeitet die Audio-Daten...")
        text = recognizer.recognize_google(audio, language="de-DE")
        return text
    except sr.UnknownValueError:
        return "Entschuldigung, das habe ich nicht verstanden."
    except sr.RequestError:
        return "Fehler: Verbindung zum Erkennungsdienst fehlgeschlagen."


if __name__ == "__main__":
    speak("Ich bin jetzt online. Was kann ich für dich tun.")

    command = listen()
    print(f"Befehl: {command} erhalten.")

    if "notepad" in command or "editor" in command:
        speak("Ich öffne Notepad.")
        os.system("notepad.exe")
    elif "editor" in command:
        speak("Ich öffne Editor.")
        os.system("editor.exe")
    elif command == "":
        speak("Ich konnte dich nicht verstehen.")
    else:
        speak("Ich bin jetzt erhalten.")

