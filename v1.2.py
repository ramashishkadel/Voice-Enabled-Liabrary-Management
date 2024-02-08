import sqlite3
import pyttsx3
import smtplib
import random
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
    def selectbook(self,bookName):
        b = conn.cursor()
        b.execute(f"select * from library where Book_Name = '{bookName.lower()}'")
        z = b.fetchall()
        if len(z) == 0:
            print(f"No Such Book as {str(bookName).capitalize()}")
            #speak(f"No Such Book as {str(bookName).capitalize()}")
            print("Try Again")
            #speak("Try Again")
        else:
            for i in range(len(z)):
                print(f"Book Name: {str(z[0][1]).capitalize()}.")
                #speak(f"Book Name {str(z[0][1]).capitalize()}.")
                print(f"Author Name: {z[0][2]}")
                #speak(f"Author Name {z[0][2]}")
                print(f"Description of Book: {z[0][4]}")
                #speak(f"Description of Book {z[0][4]}")
                print(f"Do you want to take {bookName.upper()} ?")
                bookQuery = input("--> ")
                if bookQuery == "yes":
                    r = register()
                    r.bookRegister(bookName)
                elif bookQuery == "no":
                    pass


class register:
    def bookRegister(self,bookName):
        e = conn.cursor()
        print(f"Do you want to take book or mail you pdf ?")
        bookQuery1 = input("-->")
        if bookQuery1 == "take book":
            e.execute(f"""select Availability from library where Book_Name = '{bookName.lower()}'""")
            ifAvail = e.fetchall()
            if ifAvail[0][0] == 1:
                print("Book not Available.")
            elif ifAvail[0][0] == 0:
                e.execute(f"""UPDATE library SET Availability = 1 WHERE Book_Name = '{bookName.lower()}';""")
                print("Books is registered for you.")
        elif bookQuery1 == "mail":
            try:
                d = conn.cursor()
                d.execute(f"select Book_link from library where Book_Name = '{bookName.lower()}'")
                z = d.fetchall()
                link = str(f"{z[0][0]}")
                if link == "NULL":
                    print("E-book not available.")
                else:
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


class categoryClass:
    def categorySort(self,category):
        c = conn.cursor()
        c.execute(f"select Book_Name,Rating from library where Category = '{category}'")
        cateStore = c.fetchall()
        if len(cateStore) == 0:
            print(f"No Such category as {category}")
            #speak(f"No Such category as {categoryInput}")
            print("Try Again")
            #speak("Try Again")
        else:
            #speak(f"Books in {str(categoryInput).capitalize()}")
            index = random.randint(0,len(cateStore)-1)
            print(f"System recommended {str(cateStore[index][0]).upper()}, with rating {str(cateStore[index][1])}/10.")
            print()
            print("Do you wanna take book ? ")
            registerBook = input("-->").lower()
            if registerBook == "yes":
                r = register()
                bookname = cateStore[index][0]
                r.bookRegister(bookname)
            elif registerBook == "no":
                pass
            print()

#

while True:
    print()
    print("Select a command.")
    #speak("Select a command.")
    print(f">> Search a book you wanna search.")
    print(f"e.g. search love in the time of cholera.")
    print()
    #speak(f"[1]-Search a book you wanna search.")
    print(f">> Suggest a book with category.")
    print(f"e.g. suggest fantasy.")
    print()
    #speak("Type category to Display a book according to genre.")
    print(f">> Type quit to end program.")
    print()
    #speak("Type quit to end program.")
    function = input("--> ").lower()
    task = function.split(" ",1)
    print()
    if task[0].lower() == "search":
        bookName = task[1]
        a = searchBook()
        a.selectbook(bookName)

    elif task[0].lower() == "quit":
        print("Thanks for your time")
        #speak("Thanks for your time")
        break
    elif task[0].lower() == "suggest":
        category = task[1]
        b = categoryClass()
        b.categorySort(category)
    else:
        #speak("Not a command repeat again.")
        print("Not a command repeat again")

conn.commit()
conn.close()