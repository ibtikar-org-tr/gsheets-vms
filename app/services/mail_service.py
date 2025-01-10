import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

def send_email(to, subject, message):
    SMTP_PORT = os.getenv('SMTP_PORT')
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASS = os.getenv('SMTP_PASS')
    SMTP_HOST = os.getenv('SMTP_HOST')

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()

        print(f"Email sent successfully to {to}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_sms(phone, message):
    try:
        SMS_MS = os.getenv('SMS_MS')
        if SMS_MS:
            response = requests.post(f"{SMS_MS}?phone={phone}&message={message}")
            response.raise_for_status()
            print("SMS sent successfully to ", phone)
        else:
            print("SMS_MS not set, SMS not sent")
            return
    except requests.exceptions.RequestException as e:
        print(f"Failed to send SMS: {e}")

def send_notification(username, projectname, title, content):
    try:
        NOTIFICATION_MS = os.getenv('NOTIFICATION_MS')
        response = requests.post(f"{NOTIFICATION_MS}?username={username}&projectname={projectname}&title={title}&content={content}")
        response.raise_for_status()
        print("Notification sent successfully to ", username)
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Notification: {e}")