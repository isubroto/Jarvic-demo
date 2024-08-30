import pyttsx3
import  datetime
import speech_recognition as sr
import wikipedia
import requests
import json
from newsapi import NewsApiClient
import webbrowser
import os
import pywhatkit as kit
engine=pyttsx3.init("sapi5")

voice=engine.getProperty("voices")

engine.setProperty("voice", voice[1].id)
newsapi = NewsApiClient(api_key='5e173bda505b40d4b6aa9e8b2d726130')


def speak(audio):
    """
    This function uses to convert the given text into speech.

    Parameters:
    audio (str): The text to be converted into speech.

    Returns:
    None: The function does not return any value. It use to speak the given text.
    """
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """
    This function is used to wish the user based on the current time.

    Parameters:
    None: This function does not take any parameters.

    Returns:
    None: The function does not return any value. It use to wish the user.
    """
    
    hour =int(datetime.datetime.now().hour)
    if hour > 0 and hour <12:
        speak(f"Good Morning Subroto")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon Subroto")
    else:
        speak(f"Good Evening Subroto")
    speak(f" I am Jarvis, Please tell me how can i help you?")

def takeCommand():
    """
    This function is used to capture voice commands and convert them into text.

    Parameters:
    None: This function does not take any parameters. It uses the microphone to capture audio input.

    Returns:
    str: The function returns a string representing the recognized text from the voice command.
         If the recognition fails, it returns "none".
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio)
            print(f"user said {query} \n")
        except Exception as e:
            print(f"Sorry Subroto Say Again")
            return "none"
    return query
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' and 'who' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            query = query.replace("who", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(result)
        
        elif 'news' in query:
            speak('News Headings')
            query = query.replace("news", "")
            news = newsapi.get_everything(q='apple' if 'apple' and 'iphone' in query else
                                        'google' if 'google' and 'android' in query else
                                        'tesla' if 'tesla' in query else
                                        '', sort_by='publishedAt')
            articles = news["articles"]
            for count, article in enumerate(articles[:10], 1):
                speak(article["title"])
                speak(article["description"])
                if count != len(articles):
                    speak("Moving on to the next news article")
            speak("anything else?")
        
        elif 'open' in query:
            speak("Opening...")
            sites = {
                'google': "https://www.google.com/",
                'youtube': "https://www.youtube.com/",
                'wikipedia': "https://en.wikipedia.org/",
                'facebook': "https://www.facebook.com/",
                'instagram': "https://www.instagram.com/",
                'twitter': "https://x.com/",
                'github': "https://github.com/",
                'linkedin': "https://www.linkedin.com/",
                'stackoverflow': "https://stackoverflow.com/",
                'discord': "https://discord.com/",
                'gmail': "https://mail.google.com/",
                'tumblr': "https://www.tumblr.com/",
                'pinterest': "https://www.pinterest.com/",
                'whatsapp': "https://web.whatsapp.com/",
                'reddit': "https://www.reddit.com/",
                'google drive': "https://www.google.com/drive/",
                'outlook': "https://outlook.com/",
                'zoho': "https://www.zoho.com/",
                'netflix': "https://www.netflix.com/",
                'apple': "https://www.apple.com/",
                'amazon': "https://www.amazon.com/",
                'ebay': "https://www.ebay.com/",
                'apple pay': "https://apple.com/apple-pay/",
                'zoho mail': "https://mail.zoho.com/"
            }
            for site, url in sites.items():
                if site in query:
                    webbrowser.open(url)
                    speak(f"I have opened {site} for you.")
                    break
            else:
                speak("I am not able to open this website. Please check the spelling and try again.")
                speak("anything else?")
        
        elif 'search' and 'search in browser' in query:
            speak('What do you want to search?')
            web_query = takeCommand().lower()
            web_url = f"https://www.google.com/search?q={web_query}"
            webbrowser.open(web_url)
            speak(f"I have opened {web_query} for you.")
            speak("anything else?")
        
        elif 'weather' and 'in' in query:
            speak('City name?')
            city_name = takeCommand().lower()
            api_key = "8e6a087ce7f01ae91d068390473d3dca"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            data = response.json()
            if data["cod"] != "404":
                main = data["main"]
                temperature = main["temp"] - 273.15
                humidity = main["humidity"]
                temp_max = main["temp_max"] - 273.15
                temp_min = main["temp_min"] - 273.15
                weather_desc = data["weather"][0]["description"]
                speak(f"In {city_name}, the current temperature is {temperature:.2f}°C humidity is {humidity} maximum Temperature is {temp_max:.2f}°C minimum Temperature is {temp_min:.2f}°C and {weather_desc}.")
            else:
                speak("City Not Found")
            speak("anything else?")
        
        elif 'ip' and 'ip address' and 'ip details' in query:
            ip_address = requests.get('https://api.ipify.org').text
            ip_info = requests.get(f'https://geo.ipify.org/api/v2/country?apiKey=at_Kvdmvmd0o1oqjyzUCbal81qeNQbss&ipAddress={ip_address}').text
            country = requests.get('https://api.first.org/data/v1/countries').text
            ip_info = json.loads(ip_info)
            country = json.loads(country)
            speak(f"Your IP address is {ip_info['ip']} country is {country['data'][ip_info['location']['country']]['country']} and city is {ip_info['location']['region']} internet provider is {ip_info['isp']}")
            speak("anything else?")
        
        elif 'run' in query:
            apps = {
                'command prompt': "start cmd",
                'calculator': "calc",
                'notepad': "notepad",
                'paint': "mspaint",
                'powershell': "powershell",
                'vs code': "code",
                'chrome': "chrome",
                'edge': "edge",
                'firefox': "firefox",
                'brave': "brave",
                'explorer': "explorer"
            }
            for app, command in apps.items():
                if app in query:
                    os.system(command)
                    speak(f"I have opened {app}.")
                    break
            else:
                speak("I am not able to open this application.")
                speak("anything else?")
        
        elif 'play' in query and 'youtube' in query:
            speak('What do you want to play on YouTube?')
            video_query = takeCommand().lower()
            kit.playonyt(video_query)
        
        elif 'search' in query and 'youtube' in query:
            speak('What do you want to search on YouTube?')
            video_query = takeCommand().lower()
            web_url = f"https://www.youtube.com/results?search_query={video_query}"
            webbrowser.open(web_url)
            speak(f"I have searched for {video_query} on YouTube.")
            speak("anything else?")
        
        elif 'search' in query:
            speak('What do you want to search on Google?')
            search_query = takeCommand().lower()
            web_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(web_url)
            speak(f"I have searched for {search_query} on Google.")
        elif 'quit' in query or 'exit' in query or 'see you' in query or 'bye' in query or 'goodbye' in query:
            speak("Goodbye! Have a great day.")
            exit()
        elif 'joke' in query or 'jocks' in query:
            response = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
            results = response.json()
            print(results)
        else:
            speak("I am sorry, I did not understand that. anything else?")
             
        
                