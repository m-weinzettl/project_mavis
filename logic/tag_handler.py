import random
import subprocess
from datetime import datetime
import requests

def handle_tag(tag, intent, speak):
    if tag == "open_notepad":
        speak(random.choice(intent['responses']))
        subprocess.Popen("notepad.exe", shell=True)

    elif tag == "close_notepad":
        speak(random.choice(intent['responses']))
        subprocess.Popen("taskkill /f /im notepad.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elif tag == "get_time":
        now_hour = datetime.now().strftime("%H")
        now_minute = datetime.now().strftime("%M")
        antwort = random.choice(intent['responses'])
        speak(f"{antwort} {now_hour} Uhr {now_minute}.")

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
        subprocess.Popen("powershell -Command \"$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]174)\"", shell=True)

    elif tag == "volume_mute":
        speak(random.choice(intent['responses']))
        subprocess.Popen("powershell -Command \"(New-Object -ComObject WScript.Shell).SendKeys([char]173)\"", shell=True)

    elif tag == "open_browser":
        speak(random.choice(intent['responses']))
        subprocess.Popen("cmd /c start microsoft-edge:", shell=True)

    elif tag == "open_explorer":
        speak(random.choice(intent['responses']))
        subprocess.Popen("explorer.exe", shell=True)

    elif tag == "open_calculator":
        speak(random.choice(intent['responses']))
        subprocess.Popen("calc.exe", shell=True)

    elif tag == "open_taskmanager":
        speak(random.choice(intent['responses']))
        subprocess.Popen("taskmgr.exe", shell=True)

    elif tag == "screenshot":
        speak(random.choice(intent['responses']))
        subprocess.Popen("powershell -Command \"[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.SendKeys]::SendWait('{PRTSC}')\"", shell=True)

    elif tag == "open_cmd":
        speak(random.choice(intent['responses']))
        subprocess.Popen("start cmd.exe", shell=True)

    elif tag == "open_paint":
        speak(random.choice(intent['responses']))
        subprocess.Popen("mspaint.exe", shell=True)

    elif tag == "system_info":
        speak(random.choice(intent['responses']))
        subprocess.Popen("msinfo32.exe", shell=True)

    elif tag == "open_snippingtool":
        speak(random.choice(intent['responses']))
        subprocess.Popen("snippingtool.exe", shell=True)

    elif tag == "open_controlpanel":
        speak(random.choice(intent['responses']))
        subprocess.Popen("control.exe", shell=True)

    elif tag == "open_devicemanager":
        speak(random.choice(intent['responses']))
        subprocess.Popen("devmgmt.msc", shell=True)

    elif tag == "open_diskcleanup":
        speak(random.choice(intent['responses']))
        subprocess.Popen("cleanmgr.exe", shell=True)

    elif tag == "open_volumemixer":
        speak(random.choice(intent['responses']))
        subprocess.Popen("sndvol.exe", shell=True)

    elif tag == "pc_shutdown":
        speak(random.choice(intent['responses']))
        subprocess.Popen("shutdown /s /t 60", shell=True)

    elif tag == "pc_restart":
        speak(random.choice(intent['responses']))
        subprocess.Popen("shutdown /r /t 5", shell=True)

    elif tag == "clear_clipboard":
        speak(random.choice(intent['responses']))
        subprocess.Popen("powershell -Command \"Clear-Clipboard\"", shell=True)

    elif tag == "smalltalk_weather":
        try:
            response = requests.get("https://wttr.in/?format=%C;%t", timeout=5)
            if response.status_code == 200:
                data = response.text.split(";")
                condition = data[0].strip()
                temp = data[1].replace("+", "").strip()
                speak(f"Das aktuelle Wetter an deinem Standort zeigt: {condition} bei {temp}.")
            else:
                speak("Ich konnte keine Verbindung zum Wetterdienst herstellen.")
        except requests.RequestException:
            speak("Das Abrufen der Wetterdaten ist fehlgeschlagen.")

    elif tag == "goodbye":
        speak(random.choice(intent['responses']))

    else:
        speak(random.choice(intent['responses']))