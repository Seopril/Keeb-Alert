# Import
import os
import platform
import sys
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from twilio.rest import Client
import configparser


def email(message, email_to=None, email_from=None, email_pass=None, email_server=None, port=None):
    now = datetime.datetime.now()
    date = now.strftime("%B %d, %Y")

    msg = MIMEMultipart('alternative')
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = f"GeekHack Updates - {date}"
    msg.attach(MIMEText(message, 'html'))

    s = smtplib.SMTP_SSL(email_server, port)
    s.starttls()
    print("TLS Started")
    s.login(email_from, email_pass)
    print("Logged In")
    text = msg.as_string()
    print("Sending Mail")
    import_settings()
    s.sendmail(email_from, email_to, text)
    s.quit


def sms(message, sms_to=None, sms_from=None, twilio_id=None, twilio_key=None):
    # Instatiate Client
    client = Client(twilio_id, twilio_key)
    for i in message:
        client.messages.create(to=sms_to, from_=sms_from, body=i)
        pass   
