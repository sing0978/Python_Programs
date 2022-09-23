import getpass
import imaplib
import os
import smtplib
from tkinter import ttk
from email import message_from_string
from bs4 import BeautifulSoup
import html2text
import datetime
from os.path import *
import tkinter as tk
import re

connection = imaplib.IMAP4_SSL('imap.gmail.com')
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class authentication:
    def __init__(self, email, password, from_email):
        self.email = email
        self.from_email = from_email
        self.password = password


    def authenticate(self):
        try:
            if connection.login(self.email, self.password):
                return True
        except imaplib.IMAP4.error as error:
            return False

class reading_email(authentication):
    def __init__(self, email, password, from_email):
        authentication.__init__(self, email, password, from_email)

    def deleting_email(self):
        print("{0} Connecting to mailbox via IMAP...".format(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
        full_path = expanduser('~')
        connection.select('inbox')
        what = "FROM"
        typ, data = connection.search(None, '({} "{}")'.format(what, from_email))
        count = str(data[0], encoding='utf-8')
        if len(count) == 0:
            print("Empty Mailbox")
        elif len(count) == 1:
            print("You have a new email")
        else:
            print(f"You have {len(count)} new emails")
        for num in data[0].split():
            result, email_id = connection.fetch(num, '(RFC822)')
            raw_email = email_id[0][1]
            raw_email_string = raw_email.decode('utf-8')
            msg = message_from_string(raw_email_string)
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    print("This is a text/html email")
                    body = part.get_payload(decode=True)
                    with open(f'{full_path}/Documents/{email}.txt', "w") as f:
                        f.write(str(body))
                    # m.store(num, "+FLAGS", "\\Deleted")
                    # soup = BeautifulSoup(body, features="html.parser")
                    # text = soup.select('.padding-copy')
                    # for message in text:
                    # print('\n' + message.getText())

                elif part.get_content_type() == "text/plain":
                    print("This is a text/plain email")
                    body = part.get_payload(decode=True).decode()
                    print(body)
                    with open(f'{full_path}/Documents/{email}.txt', "w") as f:
                        f.write(str(body))
                    # m.store(num, '+FLAGS', '\\Deleted')
                else:
                    pass

email = input("Please enter your email: ")
while True:
    if re.fullmatch(regex, email):
        password = input("Please enter your password: ")
        from_email = input("Enter from email: ")
        auth = reading_email(email, password, from_email)
        while True:
            if auth.authenticate():
                print("Authentication Successful.....Deleting Emails")
                auth.deleting_email()
                break
            else:
                print(auth.authenticate())
                print("Invalid Credentials")
            email = input("Please enter your email: ")
            password = input("Please enter your password: ")
            from_email = input("Enter from email: ")
            auth = reading_email(email, password)
        break
    else:
        print("Wrong email format")
    email = input("PLease enter your email: ")




