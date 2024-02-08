import sqlite3
import pyttsx3
import smtplib
import speech_recognition as sr
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from pprint import pprint



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

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Speak")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print()
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')  # Using google for voice recognition.
            print()
            #print(f"User said: {query}\n")  # User query will be printed.

        except Exception as e:
            print()
            query = input("Sorry couldn't recognize please type your input: ")
            #print("Say that again please...")  # Say that again will be printed in case of improper voice
            #return "None"  # None string will be returned
        return query

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
                print("x-x-x-x-x-x-x-BOOK DETAILS-x-x-x-x-x-x-x-x")
                print(f"Book Name: {str(z[0][1]).capitalize()}.")
                speak(f"Book Name {str(z[0][1]).capitalize()}.")
                print("\n")
                print(f"Author Name: {z[0][2]}")
                speak(f"Author Name {z[0][2]}")
                print("\n")
                print(f"Description of Book:\n{z[0][4]}")
                #speak(f"Description of Book {z[0][4]}")
                print("\n")
                print(f"Do you want to take {bookName.upper()} ?")
                speak(f"Do you want to take {bookName.upper()} ?")
                bookQuery = takeCommand().lower()
                if bookQuery == "yes":
                    r = register()
                    r.bookRegister(bookName)
                elif bookQuery == "no":
                    pass


class register:
    def bookRegister(self,bookName):
        e = conn.cursor()
        print(f"Do you want to pick up the book or mail ebook you as pdf ?")
        speak(f"Do you want to pick up the book or mail ebook you as pdf ?")
        bookQuery1 = takeCommand().lower()
        if bookQuery1 == "pick up":
            e.execute(f"""select Availability from library where Book_Name = '{bookName.lower()}'""")
            ifAvail = e.fetchall()
            if ifAvail[0][0] == 1:
                print("Book not Available.")
                speak("Book not Available.")
            elif ifAvail[0][0] == 0:
                e.execute(f"""UPDATE library SET Availability = 1 WHERE Book_Name = '{bookName.lower()}';""")
                print("Books is registered for you.")
                speak("Books is registered for you.")
        elif bookQuery1 == "mail":
            try:
                d = conn.cursor()
                d.execute(f"select Book_link from library where Book_Name = '{bookName.lower()}'")
                z = d.fetchall()
                link = str(f"{z[0][0]}")
                if link == "NULL":
                    print("E-book not available.")
                    speak("E-book not available.")
                else:
                    content = f"""
<body style="background-color: #0FDDAf; border-radius: 30px;">
  <br>
  <center>
      <img src="https://github.com/Aamir041/VEMM/blob/main/VEL.png?raw=true" alt="VEL" style="border-radius: 70px;">

          <p style="  background-color: #379683; padding: 5px; font-family: monospace;  font-size: large; width: 300px; border-radius: 40px ; ">
              <a href="{link}" style="text-decoration: none; color: darkblue;">Click here to download <br>{bookName.title()}</a>
          </p>
      <p><h2 style="color: #123C69; font-family: 'Courier New', Courier, monospace;font-size: 20px;">&nbsp;Thank you 😍 for choosing&nbsp;<b>Voice Enabled Library</b></h2></p>
      <p style="font-size: 20px; color: #05386B; font-family:monospace;">SYIT I<sup>st</sup> SEM project by </p>
      <article style="background-color: #379683; width: 200px; border-radius: 40px; height: 70px; font-weight: bold;">
          <center><p style="font-family:monospace; font-size: 15px; color: #05386B; ;"><br><u>Aamir</u> <u>Arun</u><br>&nbsp;<u>Navid</u>&nbsp;&nbsp;<u>Shubham</u></p></center>
      </article>
  </center>
  <br>
</body>
"""

                    speak("Enter your gmail address")
                    to = input("Enter your gmail address :- ")
                    sendEmail(to, content)
                    print("Email has been sent!")
                    speak("Email has been sent!")
            except Exception as e:
                print(e)
                print("Sorry I am not able to send this email")
                speak("Sorry I am not able to send this email")


class categoryClass:
    def categorySort(self,category):
        c = conn.cursor()
        if category == "fantasea":
            category = "fantasy"
        else:
            pass
        c.execute(f"select Book_Name,Rating from library where Category = '{category}'")
        cateStore = c.fetchall()
        if len(cateStore) == 0:
            print(f"No Such category as {category}")
            speak(f"No Such category as {category}")
            print("Try Again")
            speak("Try Again")
        else:
            #speak(f"Books in {str(categoryInput).capitalize()}")
            index = random.randint(0,len(cateStore)-1)
            print(f"Book Recommended:\nName: {str(cateStore[index][0]).upper()}\nrating:{str(cateStore[index][1])}/10.")
            speak(f"Book Details \n Name: {str(cateStore[index][0]).upper()}\nrating:{str(cateStore[index][1])}by10.")
            print()
            print("Do you wanna take book ? ")
            speak("Do you wanna take book ? ")
            registerBook = takeCommand().lower()
            if registerBook == "yes":
                r = register()
                bookname = cateStore[index][0]
                r.bookRegister(bookname)
            elif registerBook == "no":
                pass
            print()
    def displayCategories(self,bookCategories):
        #categoriesOfBook = ['autobiography', 'fantasy', 'fiction', 'business', 'romantic', 'programming', 'business ', 'arts']
        space = "\t"
        b = conn.cursor()
        
        for i in range(len(bookCategories)):
            print()
            count = 1
            print("Category:- ",bookCategories[i].capitalize())
            b.execute(f"select Book_Name from library where Category = '{bookCategories[i]}'")
            z = b.fetchall()
            for j in range(len(z)):
                print(f"[{count}]",space,str(z[j][0]).title())
                count += 1
            print()
        ent = input("Press Enter To Continue..")
        print("Do you want to take book?")
        speak("Do you want to take book?")
        inp = takeCommand().lower()
        if inp == "yes":
            print("Name book you want to take ?")
            speak("Name book you want to take ?")
            nameBook = takeCommand().lower()
            takeBook1 = register()
            takeBook1.bookRegister(nameBook) 
        elif inp == "no":
            pass




while True:
    print()
    print("Select a Query.")
    #speak("Select a command.")
    print(f">> Search a book you wanna look.")
    speak(f"Search a book you want to look.")
    print(f"e.g. search love in the time of cholera.")
    print()

    print(f">> Suggest a book with category.")
    speak(f"Suggest a book with category.")
    print(f"e.g. suggest fantasy.")
    print()

    print(f">> Show categories of book available.")
    speak(f"Show categories of book available.")
    print()

    print(f">> Say quit to end program.")
    speak(f"Say quit to end program.")
    print()
    
    speak("Command the above given queries")
    function = takeCommand().lower()
    task = function.split(" ",1)
    print()
    if task[0].lower() == "search":
        bookName = task[1].lower()
        print(bookName)
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
    elif task[0].lower() == "show":
        if "categories" in task[1].lower():
            categoriesOfBook = ['autobiography','fantasy','fiction','business','romantic','programming','arts']
            a = categoryClass()
            a.displayCategories(categoriesOfBook)
        else:
            speak("Not a command repeat again.")

    else:
        print("Not a command repeat again")
        speak("Not a command repeat again.")

conn.commit()
conn.close()