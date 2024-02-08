import sqlite3
import pyttsx3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
#import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

conn = sqlite3.connect('Library.db')

def sendEmail(to, content):
    senderEmail = "group0x4@gmail.com"
    password = "aans@1234"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your Link"
    msg['From'] = senderEmail
    msg['To'] = to

    msg.attach(MIMEText(content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(senderEmail, password)
    print("Server Connected")
    server.sendmail(senderEmail, to, msg.as_string())
    server.close()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# book recommendation
class searchBook:
    def selectbook(self):
        b = conn.cursor()
        print('Type the book you wanna search.')
        speak('Type the book you wanna search.')
        book = input("> ").lower()
        b.execute(f"select * from library where Book_Name = '{book.lower()}'")
        z = b.fetchall()
        if len(z) == 0:
            print(f"No Such Book as {str(book).capitalize()}")
            speak(f"No Such Book as {str(book).capitalize()}")
            print("Try Again")
            speak("Try Again")
        else:
            for i in range(len(z)):
                print(f"Book Name: {str(z[0][1]).capitalize()}.")
                speak(f"Book Name {str(z[0][1]).capitalize()}.")
                print(f"Author Name: {z[0][2]}")
                speak(f"Author Name {z[0][2]}")
                print(f"Description of Book: {z[0][4]}")
                #speak(f"Description of Book {z[0][4]}")
                if z[0][6] == 1:
                    print("Book is not Available")
                    speak("Book is not Available")
                elif z[0][6] == 0:
                    print("Book is Available")
                    speak("Book is Available")
                    print("Do you want to take book ?")
                    speak("Do you want to take book ?")
                    booktake = input("> ").lower()
                    if booktake == "yes":
                         b.execute(f"""UPDATE library SET Availability = 1 WHERE Book_Name = '{book.lower()}';""")
                         print("Books is registered for you.")
                         speak("Books is registered for you.")
                    elif booktake == "no":
                        takemail  = input("Do you want mail book link: ")
                        if takemail == "yes":
                            try:
                                d = conn.cursor()
                                d.execute(f"select Book_link from library where Book_Name = '{book.lower()}'")
                                z = d.fetchall()
                                link = str(f"{z[0][0]}")
                                content = f"""<h3>Your Link</h3><p>Book Link: {link}</p>"""
                                print(content)
                                speak("Enter Email")
                                to = input("Enter mail: ")
                                sendEmail(to, content)
                                print("Email has been sent!")
                                speak("Email has been sent!")
                            except Exception as e:
                                print(e)
                                speak("Sorry I am not able to send this email")
                        else:
                            print(f"Book not collected")
                            speak(f"Book not collected")





class categoryClass:
    def categorySort(self):
        c = conn.cursor()
        print("Type the category you wanna see the books of.")
        speak("Type the category you wanna see the books of.")
        categoryInput = input("> ").lower()
        c.execute(f"select Book_Name,Book_ID from library where Category = '{categoryInput}'")
        cateStore = c.fetchall()
        if len(cateStore) == 0:
            print(f"No Such category as {categoryInput}")
            speak(f"No Such category as {categoryInput}")
            print("Try Again")
            speak("Try Again")
        else:
            print(f"Books in {str(categoryInput).capitalize()}")
            speak(f"Books in {str(categoryInput).capitalize()}")
            for i in range(len(cateStore)):
                print(f"Book Name: {str(cateStore[i][0]).capitalize()} and Book ID: {cateStore[i][1]}")
                speak(f"Book Name is {str(cateStore[i][0]).capitalize()} and Book ID is {cateStore[i][1]}")
                print()
            print()





i = "start"
while i!="exit":
    print()
    print("Select a command.")
    speak("Select a command.")
    print(f"[1]-Type search to search a book in library.")
    speak("Type search to search a book in library.")
    print(f"[2]-Type category to Display a book according to genre.")
    speak("Type category to Display a book according to genre.")
    print(f"[3]-Type quit to end program.")
    speak("Type quit to end program.")
    function = input("> ").lower()
    print()
    if function == "search":
        a = searchBook()
        a.selectbook()

    elif function == "quit":
        print("Thanks for your time")
        speak("Thanks for your time")
        i = "exit"

    elif function == "category":
        b = categoryClass()
        b.categorySort()
    else:
        speak("Not a command repeat again.")
        print("Not a command repeat again")

conn.commit()
conn.close()
