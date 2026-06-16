import random
import subprocess
from datetime import datetime

def handle_tag(tag, intent, speak):
    if tag == "open_notepad":
        speak(random.choice(intent['responses']))
        subprocess.Popen("notepad.exe", shell=True)

    elif tag == "close_notepad":
        speak(random.choice(intent['responses']))
        # Korrigiert von editor.exe auf notepad.exe
        subprocess.Popen("taskkill /f /im notepad.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elif tag == "get_time":
        now = datetime.now().strftime("%H:%M")
        antwort = random.choice(intent['responses'])
        speak(f"{antwort} {now} Uhr.")

    elif tag == "open_google":
        speak(random.choice(intent['responses']))
        subprocess.Popen("cmd /c start https://www.google.com", shell=True)

    elif tag == "open_windows_settings":
        speak(random.choice(intent['responses']))
        subprocess.Popen("cmd /c start ms-settings:", shell=True)

    elif tag == "volume_up":
        speak(random.choice(intent['responses']))
        subprocess.Popen("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys([char]175)\"", shell=True)

    elif tag == "volume_down":
        speak(random.choice(intent['responses']))
        subprocess.Popen("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys([char]174)\"", shell=True)

    elif tag == "volume_mute":
        speak(random.choice(intent['responses']))
        subprocess.Popen("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys([char]173)\"", shell=True)

    elif tag == "goodbye":
        speak(random.choice(intent['responses']))

    else:
        speak(random.choice(intent['responses']))