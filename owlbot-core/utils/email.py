import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
import re

def send_email(
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    subject: str,
    message: str
) -> bool:
    """
    Send an email notification.
    
    Args:
        sender_email: Sender's email address
        sender_password: Sender's email password
        recipient_email: Recipient's email address
        subject: Email subject
        message: Email message
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login and send
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def check_inbox(
    email_address: str,
    password: str,
    sender_email: str
) -> str:
    """
    Check email inbox for messages from a specific sender.
    
    Args:
        email_address: Email address to check
        password: Email password
        sender_email: Sender's email address to filter by
        
    Returns:
        Content of the most recent email from the sender, or None if none found
    """
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_address, password)
        mail.select('inbox')
        
        # Search for emails from sender
        _, data = mail.search(None, f'(FROM "{sender_email}")')
        email_ids = data[0].split()
        
        if not email_ids:
            return None
            
        # Get most recent email
        latest_email_id = email_ids[-1]
        _, data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = data[0][1]
        
        # Parse email
        email_message = email.message_from_bytes(raw_email)
        
        # Get email content
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return email_message.get_payload(decode=True).decode()
            
    except Exception as e:
        print(f"Error checking inbox: {e}")
        return None
    finally:
        try:
            mail.logout()
        except:
            pass

def check_text_confirmation(text: str) -> bool:
    """
    Check if a text message contains a confirmation.
    
    Args:
        text: Text to check
        
    Returns:
        True if text contains confirmation, False otherwise
    """
    if not text:
        return False
        
    # Look for confirmation patterns
    confirmation_patterns = [
        r'\b(?:yes|ok|confirmed|acknowledged|received)\b',
        r'\b(?:i confirm|i acknowledge|i received)\b',
        r'\b(?:that\'s fine|sounds good|got it)\b'
    ]
    
    text = text.lower()
    return any(re.search(pattern, text) for pattern in confirmation_patterns) 