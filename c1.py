from datetime import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import requests

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        rec.pause_threshold = 1
        audio = rec.listen(source)
        try:
            query = rec.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except Exception:
            return ""

greet_msgs = ["hi", "hello", "hey", "hi there"]
date_msgs = ["date", "today", "what is the date"]
time_msgs = ["time", "what is the time"]
site_msgs = ["youtube", "google", "facebook", "instagram", "twitter", "cybervidya"]
news_msgs = ["tell me news", "news", "headlines"]

def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=695e07af402f4b119f0703e9b19f4683"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])
        for i, article in enumerate(articles[:3]):
            speak(f"Headline {i+1}: {article['title']}")
    except Exception:
        speak("I am unable to fetch news at the moment.")

chat = True
speak("Hello, I am your assistant. How can I help you?")

while chat:
    user_msg = listen()

    if not user_msg:
        continue

    if any(msg in user_msg for msg in greet_msgs):
        speak("Hello! How may I help you?")
    elif any(msg in user_msg for msg in news_msgs):
        get_news()
    elif any(msg in user_msg for msg in date_msgs):
        speak(f"Today's date is: {datetime.now().strftime('%B %d, %Y')}")
    elif any(msg in user_msg for msg in time_msgs):
        speak(f"Current time is: {datetime.now().strftime('%I:%M %p')}")
    elif any(site in user_msg for site in site_msgs):
        for site in site_msgs:
            if site in user_msg:
                speak(f"Opening {site}...")
                webbrowser.open(f"https://www.{site}.com")
                break
    elif "calculate" in user_msg:
        try:
            expression = user_msg.replace("calculate", "").strip()
            # Basic safety for eval
            result = eval(expression, {"__builtins__": None}, {})
            speak(f"The result is: {result}")
        except Exception:
            speak("I couldn't calculate that expression.")
    elif "bye" in user_msg or "stop" in user_msg:
        speak("Bye! Have a great day!")
        chat = False
    else:
        speak("I'm sorry, I didn't understand that.")