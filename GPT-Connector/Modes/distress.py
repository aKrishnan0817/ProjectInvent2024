import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
import time

import os
import sys
sys.path.append('../')
#import sensitiveData

from toolkit.distressTools import distressTools

from gptMessagePrepare import prepare_message
from TTS import ttsPlay



def send_email(sender_email, sender_password, recipient_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()

    except Exception as e:
        print(f"Error: {e}")

def extract_plain_text(raw_msg):
    raw_msg = str(raw_msg)
    msg = raw_msg[raw_msg.find("<td>")+len("<td>") : raw_msg.find("</td>")].replace(" ", "")
    print(msg)

    return msg

# Function to check email inbox for confirmation
def check_inbox(username, password, sender):
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username, password)
        mail.select('inbox')

        # Search for unseen emails
        result, data = mail.search(None, 'UNSEEN')
        ids = data[0].split()

        for email_id in ids:
            result, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract sender's email address
            sender_email = msg['From']

            email_str = raw_email.decode('utf-8')
            message = email.message_from_string(email_str)

            # Check if the email is from the expected sender and contains the confirmation keyword
            #print(message)
            text = extract_plain_text(message)
            if sender in sender_email :
                #print("Confirmation received from", sender_email)
                return text
            else:
                print('Confirmation not yet received')


        mail.logout()
    except Exception as e:
        print("Error:", e)
        return None

def checkTextConfirmation(text):
    iprompt = []
    assert1={"role": "system", "content": "You are a robot looking for confirmation"}
    assert2={"role": "assistant", "content": "You are attempting to check if the user is confirming a text message"}
    iprompt.append(assert1)
    iprompt.append(assert2)
    iprompt.append({"role": "user", "content": text})
    _,_,confirmation = prepare_message(iprompt, 2 , distressTools)
    if confirmation == "CONFIRMED":
        return True
    return False

def distressMode(email, password, gaurdianEmail):
    message = "Hi Hope, this is a notification that Jonah may be in a distressed state right now. Please check in on him as soon as you can."
    subject = 'AI Companion: Notification for Jonah'
    send_email(email,password,gaurdianEmail,subject, message)

    while True:
        text = check_inbox(email, password, gaurdianEmail)

        if text!= None:
            if checkTextConfirmation(text):
                print("Received Confirmation")
                break
        time.sleep(20)
