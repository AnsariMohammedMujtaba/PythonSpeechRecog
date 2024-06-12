# main.py
import os
import openai
from config import apikey
import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr

openai.api_key = apikey

chatStr = ""

def chat(query):
    global chatStr
    try:
        print(chatStr)
        openai.api_key = apikey
        chatStr += f"Mujtaba: {query}\n Jarvis: "
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chatStr}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response["choices"][0]["message"]["content"]
        say(response_text)
        chatStr += f"{response_text}\n"
        return response_text
    except openai.error.InvalidRequestError as e:
        print(f"Error: {e}")
        say("Sorry, you have exceeded your quota. Please check your plan and billing details.")
    except Exception as e:
        print(f"Error: {e}")
        say("Sorry, I couldn't process the chat request.")

def ai(prompt):
    try:
        openai.api_key = apikey
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
        text += response["choices"][0]["message"]["content"]
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)
    except openai.error.InvalidRequestError as e:
        print(f"Error: {e}")
        say("Sorry, you have exceeded your quota. Please check your plan and billing details.")
    except Exception as e:
        print(f"Error: {e}")
        say("Sorry, I couldn't process the AI request.")

def say(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        print("Could not use text-to-speech feature.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Error: {e}")
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "open music" in query:
            musicPath = "path_to_your_music_file.mp3"
            os.system(f"start {musicPath}")
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} bajke {min} minutes")
        elif "open facetime".lower() in query.lower():
            os.system(f"start explorer shell:appsFolder\Microsoft.FaceTime_8wekyb3d8bbwe!App")
        elif "open pass".lower() in query.lower():
            os.system(f"start path_to_pass_app.exe")
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Jarvis Quit".lower() in query.lower():
            exit()
        elif "reset chat".lower() in query.lower():
            chatStr = ""
        else:
            print("Chatting...")
            chat(query)
