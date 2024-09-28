import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import time
import pygame
import threading

# Initialize the voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index to 1 for female voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How can I help you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 2
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {command}\n")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError as e:
            speak(f"Could not request results from Google Speech Recognition service; {e}")
            return "None"
        except Exception as e:
            speak(f"Error: {e}")
            return "None"

def play_music():
    global playing_music
    music_dir = 'path_to_music_directory'  # Replace with the path to your music directory
    songs = [song for song in os.listdir(music_dir) if song.endswith('.mp3')]
    print(f"Songs found: {songs}")
    if songs:
        pygame.mixer.init()
        for song in songs:
            if not playing_music:
                break
            print(f"Playing song: {song}")
            song_path = os.path.join(music_dir, song)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if not playing_music:
                    pygame.mixer.music.stop()
                    break
                time.sleep(1)
    else:
        speak("No music files found in the specified directory.")
        print("No music files found in the specified directory.")

def open_website(url):
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Adjust the path if necessary
    webbrowser.get(chrome_path).open(url)

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't some couples go to the gym? Because some relationships don't work out!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "I'm reading a book on anti-gravity. It's impossible to put down!"
    ]
    speak(random.choice(jokes))

def calculate(expression):
    try:
        # Replace spoken words with mathematical operators
        expression = expression.replace("plus", "+")
        expression = expression.replace("minus", "-")
        expression = expression.replace("times", "*")
        expression = expression.replace("multiplied by", "*")
        expression = expression.replace("divided by", "/")
        expression = expression.replace("over", "/")
        expression = expression.replace("raised to the power of", "**")
        expression = expression.replace("to the power of", "**")
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Error in calculation: {e}")
        return "I am sorry, I cannot calculate that."

def open_application(app_name):
    app_paths = {
        "notepad": "C:/Windows/system32/notepad.exe",
        "calculator": "C:/Windows/system32/calc.exe",
        "paint": "C:/Windows/system32/mspaint.exe",
        "wordpad": "C:/Program Files/Windows NT/Accessories/wordpad.exe",
        "vlc": "C:/Program Files/VideoLAN/VLC/vlc.exe",
        "roblox": "C:/Path/To/Roblox/RobloxPlayerLauncher.exe",  # Replace with the actual path to Roblox
        "tlauncher": "C:/Path/To/TLauncher/TLauncher.exe",       # Replace with the actual path to TLauncher
        "ldplayer9": "C:/Path/To/LDPlayer9/LDPlayer.exe"          # Replace with the actual path to LDPlayer 9
        # Add paths to other applications as needed
    }
    
    if app_name in app_paths:
        os.startfile(app_paths[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"Sorry, I don't know how to open {app_name}")

def run_jarvis():
    global playing_music, music_thread
    wish_me()
    while True:
        command = take_command()
        if command == "none":
            continue

        if 'hi jarvis' in command or 'hello jarvis' in command:
            speak("Hello!")

        elif 'how are you' in command:
            speak("I'm doing well, thank you. How can I assist you today?")

        elif 'thank you' in command or 'thanks' in command:
            speak("You're welcome!")

        elif 'what is your name' in command:
            speak("My name is Jarvis.")

        elif 'wikipedia' in command:
            speak("Searching Wikipedia...")
            command = command.replace("wikipedia", "")
            results = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in command:
            open_website("https://www.youtube.com")

        elif 'open google' in command:
            open_website("https://www.google.com")

        elif 'open stack overflow' in command:
            open_website("https://www.stackoverflow.com")

        elif 'play music' in command:
            if not playing_music:
                print("Starting music...")
                playing_music = True
                music_thread = threading.Thread(target=play_music)
                music_thread.start()

        elif 'stop the music' in command or 'stop the song' in command:
            if playing_music:
                print("Stopping music...")
                playing_music = False
                if music_thread is not None:
                    music_thread.join()
                pygame.mixer.music.stop()
                speak("Music stopped.")

        elif 'the time' in command:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {strTime}")

        elif 'quit' in command or 'exit' in command:
            speak("Goodbye!")
            if playing_music:
                playing_music = False
                if music_thread is not None:
                    music_thread.join()
            break

        elif 'who are you' in command:
            speak("I am Jarvis, your personal assistant.")

        elif 'who created you' in command:
            speak("I was created by a developer using Python.")

        elif 'tell me a joke' in command:
            tell_joke()

        elif 'what can you do' in command:
            speak("I can help with various tasks such as searching the web, playing music, telling jokes, and more.")

        elif 'open chrome' in command:
            speak("Opening Google Chrome")
            open_website("https://www.google.com")

        elif 'goodbye' in command:
            speak("Goodbye! Have a great day!")
            if playing_music:
                playing_music = False
                if music_thread is not None:
                    music_thread.join()
            break

        elif 'calculate' in command or 'what is' in command:
            command = command.replace("calculate", "").replace("what is", "").replace("jarvis", "").strip()
            result = calculate(command)
            speak(f"The result is {result}")

        elif 'open' in command:
            app_name = command.replace("open", "").strip()
            open_application(app_name)

        else:
            speak("I'm sorry, I don't know how to respond to that. Please try a different command.")

if __name__ == "__main__":
    global playing_music
    playing_music = False
    music_thread = None
    run_jarvis()
