import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

sender_email = "pptprojectinvent@hotmail.com"
sender_password = "bgrjaxgjfhrfodex" #app password bgrjaxgjfhrfodex
recipient_email = 'pptprojectinvent@gmail.com' #temporary

smtp_server = "smtp.office365.com"
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

send_email('test','hello world')