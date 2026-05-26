import random
import subprocess
from datetime import datetime


def handle_tag(tag, intent, speak):
    if tag == "open_notepad":
        speak(random.choice(intent['responses']))
        subprocess.Popen("editor.exe", shell=True)

    elif tag == "close_notepad":
        speak(random.choice(intent['responses']))
        subprocess.Popen("taskkill /f /im editor.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elif tag == "get_time":
        now = datetime.now().strftime("%H:%M")
        antwort = random.choice(intent['responses'])
        speak(f"{antwort} {now} Uhr.")

    elif tag == "goodbye":
        speak(random.choice(intent['responses']))

    else:
        speak(random.choice(intent['responses']))