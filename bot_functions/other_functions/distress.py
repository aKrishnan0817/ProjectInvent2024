import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "pptprojectinvent@gmail.com"
sender_password = "tnms trfx seki wukx" #app password bgrjaxgjfhrfodex for 365, tnms trfx seki wukx for google
recipient_email = 'pptprojectinvent@gmail.com' #temporary

smtp_server = "smtp.gmail.com"
smtp_port = 587

def send_email(subject,body):

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


#next step would be to engineer a different prompt for when in distress mode
def main():
    #we could have different messages for different severities but that isn't necessary at this moment
    message = "Hi Hope, this is a notification that Jonah may be in a nervous state right now. Please check in on him as soon as you can."
    subject = 'AI Companion: Notification for Jonah'
    send_email(subject, message)

    prompt = "You are now operating as a therapist who is consoling and helping a child in a moment of severe distress. We already contacted his mother who is on her way."
    #return a new prompt for operating 
    return prompt 