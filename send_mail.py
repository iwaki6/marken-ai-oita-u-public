import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = os.environ['MARKEN_MAIL_ADDRESS'] 
password = os.environ['MARKEN_MAIL_PASSWORD']  

def send_passcode(passcode, recipient):
 
    msg = MIMEMultipart('mixed')

    sender = username

    msg['Subject'] = 'Your Passcode'
    msg['From'] = sender
    msg['To'] = recipient

    text_message = MIMEText(make_message(passcode), 'plain')
    # html_message = MIMEText('It is a html message.', 'html')
    msg.attach(text_message)
    # msg.attach(html_message)

    mailServer = smtplib.SMTP('smtp.office365.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(sender, recipient, msg.as_string())
    mailServer.close()

    return

def make_message(passcode):
    message = "marken-ai-oita-u sends your passcode: "+str(passcode)+"\n"
    message += "The passcode will be expired in 5 minutes."
    return message

