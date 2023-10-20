import smtplib
import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
import json

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change the index to select a different voice

# Function to speak the assistant's response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to send an email
def send_email(to, subject, body):
    # You need to allow less secure apps in your Google Account settings to use this feature
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail('your_email@gmail.com', to, message)
        server.close()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")

# Function to get the current weather
def get_weather(city):
    api_key = "your_openweathermap_api_key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] == 200:
        weather_info = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(f"The weather in {city} is {weather_info}. The temperature is {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")

# Function to answer questions using Wikipedia
def get_wikipedia_summary(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("I found multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError as e:
        speak("I couldn't find any information on that topic.")

# Function to open a website
def open_website(url):
    webbrowser.open(url)

# Function to set a reminder
def set_reminder(reminder_text, time):
    try:
        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=int(time))
        speak(f"Reminder set for {reminder_text} in {time} minutes.")
        # You can implement a reminder system here, e.g., sending notifications
    except ValueError:
        speak("Sorry, I couldn't set the reminder. Please provide a valid time.")

# Main function to handle user commands
def assistant():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("How can I assist you today?")
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command)
        
        if 'send email' in command:
            speak("Whom do you want to send an email to?")
            to = input("Recipient: ")
            speak("What should be the subject of the email?")
            subject = input("Subject: ")
            speak("Please tell me the content of the email.")
            body = input("Body: ")
            send_email(to, subject, body)
        
        elif 'weather' in command:
            speak("Sure, please tell me the city name.")
            city = input("City: ")
            get_weather(city)
        
        elif 'wikipedia' in command:
            speak("What do you want to know about?")
            query = input("Search: ")
            get_wikipedia_summary(query)
        
        elif 'open website' in command:
            speak("Please provide the URL.")
            url = input("URL: ")
            open_website(url)
        
        elif 'reminder' in command:
            speak("What should I remind you about?")
            reminder_text = input("Reminder: ")
            speak("In how many minutes?")
            time = input("Time (in minutes): ")
            set_reminder(reminder_text, time)
        
        else:
            speak("Sorry, I didn't understand your request. Can you please repeat it?")
    
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Can you please repeat your request?")
    except sr.RequestError as e:
        speak("I'm having trouble processing your request. Please try again later.")

if __name__ == "__main__":
    assistant()
