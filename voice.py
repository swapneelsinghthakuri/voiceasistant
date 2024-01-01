from logging.config import listen
import pyttsx3 as p
import speech_recognition as sr
import datetime as dt
import pyowm as OWM
import webbrowser as wb
import os as os
import smtplib as smtp

sound = p.init('sapi5')
voices = sound.getProperty('voices')
sound.setProperty('voice',voices[1].id)
#define the audio 
def speak(audio):
    sound.say(audio)
    sound.runAndWait()
#define greetings (goodmorning/goodafternoon/goodevening/goodnight according to time)
def greeting():
    hour = int(dt.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    elif hour>=18 and hour<22:
        speak("Good Evening")    
    else:
        speak("Good Night!")

    speak("Namaste iam Sudha. iam your Nepali Voice assitance how may i help you")
#define command to assitance 
def command():

    mic =sr.Recognizer()
    with sr.Microphone()as source:
        print("listening...")
        mic.pause_threshold = 1
        audio = mic.listen(source)
    
    try:
        print("Recognizing...")
        question = mic.recognize_google(audio, language='en-in')
        print(f"user said: {question}\n")

    except Exception as e:
        print("Can you Repeat i couldn't get")
        speak("Can you Repeat? i couldn't get other wise please try again later.")
        return "none"
    return question
def send_email(to, subject, body):
    msg = smtp.SMTP('smtp.gmail.com',587)
    msg.ehlo()
    msg.starttls()
    msg.login('your_email@gmail.com','your_password')
    message=f"subject: {subject}\n\n{body}"
    msg.sendmail('your_email@gmail.com', to, message)
    msg.quit()
    speak("Email sent Successfully.")
def get_weather(city):
    owm= OWM('your_openweathermap_api_key')
    wethermanger = owm.weather_manager()
    observation = wethermanger.weather_at_place(city)
    w = observation.weather
    temperature =w.temperature('celsius')['temp']
    status = w.status
    speak(f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius.")

if __name__== "__main__":
    greeting()
    while True:
        question = command().lower()


#executing task base on command
        
        if 'hello' in question:
            speak('Hello Dear, How i can answer you?')
                
        elif 'open youtube' in question:
            wb.open("youtube.com")
        elif 'open google' in question:
            wb.open("google.com")
        elif 'play song' in question:
            sound_dir = "C:\\Users\\singh\OneDrive\\Documents\\Voice Assistant"
            song = [file for file in os.listdir(sound_dir) if file.lower().endswith('.mp3')]
            if song:
                print(f"Playing: {song[0]}")
                os.startfile(os.path.join(sound_dir, song[0]))
            else:
                print("No MP3 files found in the specified directory.")
        elif 'get time' in question:
            strTime = dt.datetime.now().strftime("%H:%M:%S")
            speak(f"The Current Time is {strTime}")
        elif 'get date' in question:
            strdate = dt.datetime.now().strftime("%Y-%m-%d")
            speak(f"The Current Time is {strdate}")
        elif "email" in question:
            speak("To whom do you want to send a mail")
            recipient = listen()
            speak("what should be the subject of mail")
            email_subject = listen()
            speak("please dictate the body of the email.")
            email_body = listen()
            send_email(recipient, email_subject,email_body)
        elif "weather" in question:
            speak("Sure which city would you like to check the weather for")
            city=listen()
            if city:
                get_weather(city)
        elif "exit" or "bye" in question:
                speak("Goodbye! Have a great day.")
                quit()

     