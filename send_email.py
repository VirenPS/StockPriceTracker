import smtplib
import ssl


class Email:
    def __init__(self, subject, receiver_email, body, sender_email):
        self.subject = subject
        self.receiver_email = receiver_email
        self.password = 'Testing123!'
        self.body = body
        self.sender_email = sender_email

    def send_email(self):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"

        message = f"""Subject:{self.subject}

        {self.body}"""

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, message)
