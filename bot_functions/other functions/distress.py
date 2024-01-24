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

send_email('test','hello world')