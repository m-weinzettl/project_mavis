import random
import subprocess

def handle_tag(tag, intent, speak):
    if tag == "open_notepad":
        speak(random.choice(intent['responses']))
        subprocess.Popen(["editor.exe"])
    elif tag == "close_notepad":
        speak(random.choice(intent['responses']))
        subprocess.Popen(["close.exe"] or ["kill.exe"] or ["kill.task"])
    elif tag == "get_time":
        speak(random.choice(intent['responses']))
        subprocess.Popen(["time"])
    elif tag == "goodbye":
        speak(random.choice(intent['responses']))

    else:
        speak(random.choice(intent['responses']))

