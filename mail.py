import os
from dotenv import load_dotenv
import smtplib

load_dotenv()


class Mail:

    def __init__(self, data):
        self.data = data
        self.my_email = os.getenv("email_")
        self.password = os.getenv("email_key")
        self.send_mail()

    def send_mail(self):
        mail = f"Name: {self.data['name']}\nEmail: {self.data['email']}\n" \
               f"Phone No.: {self.data['phone']}\nMessage: {self.data['message']}"
        with smtplib.SMTP("smtp.gmail.com", port=587, timeout=999) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            connection.sendmail(
                from_addr=self.my_email,
                to_addrs=self.my_email,
                msg=f"subject: JOE'S BLOG\n\n{mail}".encode('utf-8')
            )
