import sqlite3
import pyttsx3
import speech_recognition as sr
import smtplib
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

conn = sqlite3.connect('Library.db')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')  # Using google for voice recognition.
            print(f"User said: {query}\n")  # User query will be printed.

        except Exception as e:
            # print(e)
            print("Say that again please...")  # Say that again will be printed in case of improper voice
            return "None"  # None string will be returned
        return query

# book recommendation
class searchBook:
    def selectbook(self):
        b = conn.cursor()
        print('Say the book you wanna search.')
        speak('Say the book you wanna search.')
        book = takeCommand()
        b.execute(f"select * from library where Book_Name = '{book.lower()}'")
        z = b.fetchall()
        if len(z) == 0:
            print(f"No Such Book as {str(book).capitalize()}")
            speak(f"No Such Book as {str(book).capitalize()}")
            print("Try Again")
            speak("Try Again")
            a.selectbook()
        else:
            for i in range(len(z)):
                print(f"Book Name: {str(z[0][1]).capitalize()}.")
                speak(f"Book Name {str(z[0][1]).capitalize()}.")
                print(f"Author Name: {z[0][2]}")
                speak(f"Author Name {z[0][2]}")
                print(f"Description of Book: {z[0][4]}")
                speak(f"Description of Book {z[0][4]}")



i = "start"
while i!="exit":
    print("Select a command.")
    speak("Select a command.")
    print(f"[1]-Say search to search a book in library.")
    speak("Say search to search a book in library.")
    print(f"[2]-Say category to Display a book according to genre.")
    speak("Say category to Display a book according to genre.")
    print(f"[3]-Say quit to end program.")
    speak("Say quit to end program.")
    function = takeCommand()
    func = function.lower()
    if func == "search":
        a = searchBook()
        a.selectbook()

    elif func == "quit":
        print("Thanks for your time")
        speak("Thanks for your time")
        i = "exit"

    else:
        speak("Not a command repeat again.")
        print("Not a command repeat again")


