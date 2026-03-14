import os
from dotenv import load_dotenv

load_dotenv()

from queue_manager import dequeue_email
from gmail_sender import send_email, load_accounts
from rate_limiter import RateLimiter

limiter = RateLimiter()

load_accounts()



while True:
    email = dequeue_email()

    if email:
        limiter.wait()

        try:
            send_email(email["data"])
            print("Delivered:",
                  email["mail_from"],
                  "->",
                  email["rcpt_to"])

        except Exception as e:
            print("Send failed:", e)
