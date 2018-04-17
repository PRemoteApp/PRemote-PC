import hashlib
import sys
import pyrebase
import json
from os.path import expanduser
import os
import random
from easygui import enterbox
import webbrowser

def get_user():
    # try to get mail from terminal
    try:
        usermail = sys.argv[1]
        userpass = sys.argv[2]
        return [usermail, userpass]

    except IndexError:
        # if mail is not written on terminal while opening software
        # then check data folder and see cached mail acc
        users_info = ["", ""]
        try:
            data_file = open("data.txt", "r")
            users_info = data_file.read().replace("\n", "").split(":")
        except Exception as e:
            pass

        # if account is not cached then prompt the user to enter email
        if(users_info[0] == "" or users_info[1] == ""):
            mail_input = ""
            pass_input = ""
            while("@" not in mail_input):
                mail_input = enterbox(msg="Enter your E-Mail:", title="Sign in")
                if("@" not in mail_input):
                    print("Wrong E-Mail formatting")
            users_info[0] = mail_input
            while(len(pass_input)<5):
                pass_input = enterbox(msg="Enter your Password:", title="Sign in")
                if(len(pass_input)<5):
                    print("Please enter correct password")
            users_info[1] = pass_input

            # cache file
            data_file = open("data.txt", "w+")
            data_file.write(users_info[0]+":"+users_info[1])
        data_file.close()
        return users_info

def listen_incoming_command(data):
    command = data['data']

    if "გახსენი" in command or "ჩართე" in command or "open" in command:
        if "მუსიკა" in command or "სიმღერა" in command or "music" in command or "song" in command:
            musicFolder = expanduser("~")+"/Music/"
            songs = os.listdir(musicFolder)
            webbrowser.open(musicFolder+random.choice(songs))
        else:
            listOfQueryWords = command.split(" ")
            queryWord = ""
            for i in range(len(listOfQueryWords)):
                if i:
                    queryWord += listOfQueryWords[i]+"+"
            webbrowser.open('https://www.google.com/search?q='+queryWord+'&btnI')

def formatMail(mail):
    return mail.replace(".", ",")


# get command line arguments of mail and password
user = get_user();

firebaseConfig = json.load(open('google-services.json'))

# Initialize Firebase config
config = {
  "apiKey": firebaseConfig['client'][0]['api_key'][0]['current_key'],
  "authDomain": firebaseConfig['project_info']['project_id']+".firebaseapp.com",
  "databaseURL": "https://"+firebaseConfig['project_info']['project_id']+".firebaseio.com",
  "storageBucket": firebaseConfig['project_info']['project_id']+".appspot.com"
}

firebase = pyrebase.initialize_app(config)

# Get a refference to the auth service
auth = firebase.auth()

# Sign in
user = auth.sign_in_with_email_and_password(user[0], user[1])

# Get database instance
db = firebase.database().child('commands')

# Start 'listening' to database change
db.child(formatMail(user['email'])).stream(listen_incoming_command)
