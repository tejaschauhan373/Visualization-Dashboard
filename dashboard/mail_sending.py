import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .mail_html_text import get_confirmation_mail_html
from config import sender_mail, sender_mail_pwd

def send_mail(receiver_email: str, subject: str, id: int, time_stamp: float):
    sender_email = sender_mail
    password = sender_mail_pwd
    msg = MIMEMultipart('alternative')
    text = subject
    msg['Subject'] = "Visualize"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    html = get_confirmation_mail_html(id, time_stamp)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
