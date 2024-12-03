import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from backend.core.config import MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, EMAIL_FROM, EMAIL_FROM_NAME


env = Environment(loader=FileSystemLoader('templates'))

async def send_email(to_email: str, subject: str, reset_link: str):

    template = env.get_template('reset_password.html')
    html_content = template.render(reset_link=reset_link)


    msg = MIMEMultipart("alternative")
    msg["From"] = f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>"
    msg["To"] = to_email
    msg["Subject"] = subject


    msg.attach(MIMEText(html_content, "html"))

    # Send the email
    await aiosmtplib.send(
        msg,
        hostname=MAIL_SERVER,
        port=MAIL_PORT,
        start_tls=True,
        username=MAIL_USERNAME,
        password=MAIL_PASSWORD,
    )