import asyncio
from email.message import EmailMessage

import aiosmtplib
async def send_mail(recipient: str, subject: str, plain_content: str, html_content: str):
    admin_email = "admin@site.com"
    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    
    plaint_text_message = MIMEText(plain_content, "plain", 'utf-8')
    message.attach(plaint_text_message)
    if html_content:
        html_message = MIMEText(html_content, "html", 'utf-8')
        message.attach(html_message)    
    await aiosmtplib.send(message, host="0.0.0.0", port=1025, username=admin_email, password="password",)
    
    