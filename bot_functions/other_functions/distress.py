import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sensitiveData #this is a local file that I have in my gitignore. It is in the parent directory "ProjectInvent2024". If you want this file text me (zach)

sender_email = sensitiveData.emailAddress
sender_password = sensitiveData.emailPassword 
recipient_email = 'pptprojectinvent@gmail.com'

smtp_server = "smtp.gmail.com"
smtp_port = 587


def send_email(subject, body):
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


# next step would be to engineer a different prompt for when in distress mode
def main():
    # we could have different messages for different severities but that isn't necessary at this moment
    message = "Hi Hope, this is a notification that Jonah may be in a nervous state right now. Please check in on him as soon as you can."
    subject = 'AI Companion: Notification for Jonah'
    send_email(subject, message)

    prompt = "You are now operating as a therapist who is consoling and helping a child in a moment of severe distress. We already contacted his mother who is on her way."
    # return a new prompt for operating
    return prompt



'''
this is for checking the email inbox for a confirmation from hope before returning to the GPT connector. So I think what we need to do is actually have the chatGPT set up in this 
file so that it can operate as a standalone companion without returning to GPTConnector

import imaplib
import email
import time

# Function to check email inbox for confirmation
def check_inbox(username, password, keyword, sender):
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL('imap.example.com')
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

            # Check if the email is from the expected sender and contains the confirmation keyword
            if sender_email == sender and keyword in msg.get_payload():
                print("Confirmation received from", sender_email)
                # Take appropriate action here

        mail.logout()
    except Exception as e:
        print("Error:", e)

# Example usage
if __name__ == "__main__":
    # Set your email credentials, confirmation keyword, and expected sender
    email_username = 'your_email@example.com'
    email_password = 'your_password'
    confirmation_keyword = 'CONFIRM'
    expected_sender = 'sender@example.com'

    while True:
        check_inbox(email_username, email_password, confirmation_keyword, expected_sender)
        # Check inbox every 60 seconds
        time.sleep(60)'''
