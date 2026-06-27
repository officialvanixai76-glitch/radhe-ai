import os
import sys
import webbrowser
import subprocess
import psutil
import pyautogui
from pathlib import Path
from datetime import datetime

# Attempt to load pyttsx3 and speech_recognition dynamically to maintain robustness
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None


class VoiceAssistant:
    def __init__(self):
        # Initialize text to speech engine if available
        self.tts_engine = None
        if pyttsx3:
            try:
                self.tts_engine = pyttsx3.init()
            except Exception:
                self.tts_engine = None

    def speak(self, text: str):
        """Speak text aloud or print to console if TTS library is missing."""
        print(f"VoiceAssistant: {text}")
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception:
                pass

    def listen(self) -> str:
        """Capture microphone audio and transcribe it, or return dummy command."""
        if not sr:
            # Fallback mock command if speech recognition isn't installed
            print("VoiceAssistant: Speech Recognition module missing. Emulating command.")
            return "system info"

        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            command = r.recognize_google(audio)
            return command.lower()
        except Exception:
            return ""

    def process_command(self, command: str) -> str:
        """Process natural language/voice commands and return execution status message."""
        cmd = command.lower().strip()
        if not cmd:
            self.speak("I didn't catch any command.")
            return "No command detected."

        self.speak(f"Processing command: {cmd}")

        # Web navigation
        if "open google" in cmd:
            webbrowser.open("https://google.com")
            return "Opened Google."
        elif "open youtube" in cmd:
            webbrowser.open("https://youtube.com")
            return "Opened YouTube."
        elif "open github" in cmd:
            webbrowser.open("https://github.com")
            return "Opened GitHub."

        # App Launchers (Basic Windows executables)
        elif "open notepad" in cmd:
            subprocess.Popen("notepad.exe")
            return "Opened Notepad."
        elif "open calculator" in cmd:
            subprocess.Popen("calc.exe")
            return "Opened Calculator."

        # System Queries
        elif "cpu" in cmd or "processor" in cmd:
            usage = psutil.cpu_percent()
            msg = f"The CPU usage is currently {usage}%."
            self.speak(msg)
            return msg
        elif "ram" in cmd or "memory" in cmd:
            usage = psutil.virtual_memory().percent
            msg = f"The RAM usage is currently {usage}%."
            self.speak(msg)
            return msg
        elif "battery" in cmd:
            battery = psutil.sensors_battery()
            if battery:
                msg = f"Battery status is {battery.percent}%."
            else:
                msg = "Battery telemetry is not available."
            self.speak(msg)
            return msg
        elif "time" in cmd:
            now = datetime.now().strftime("%I:%M %p")
            msg = f"The time is {now}."
            self.speak(msg)
            return msg
        elif "date" in cmd:
            today = datetime.now().strftime("%B %d, %Y")
            msg = f"Today is {today}."
            self.speak(msg)
            return msg

        # Utility actions
        elif "screenshot" in cmd:
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            file_path = screenshots_dir / f"screenshot_{int(datetime.now().timestamp())}.png"
            pyautogui.screenshot().save(file_path)
            msg = f"Screenshot saved successfully to {file_path}."
            self.speak("Screenshot captured.")
            return msg

        # No match fallback
        msg = f"Command '{cmd}' is recognized but not supported."
        self.speak(msg)
        return msg
