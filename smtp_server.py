import smtpd
import asyncore
from queue_manager import enqueue_email
import os
from dotenv import load_dotenv

load_dotenv()


class SMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):

        email_data = {
            "mail_from": mailfrom,
            "rcpt_to": rcpttos,
            "data": data.decode()
        }

        enqueue_email(email_data)
        print("Queued email:", mailfrom, "->", rcpttos)


if __name__ == "__main__":
    port = int(os.getenv("SMTP_PORT"))
    server = SMTPServer(("0.0.0.0", port), None)

    print("SMTP Server listening on", port)
    asyncore.loop()

