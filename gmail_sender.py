import base64
import random
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os


services = []


def load_accounts():
    accounts_str = os.getenv("GMAIL_ACCOUNTS")
    accounts = [acc.strip() for acc in accounts_str.split(',')] if accounts_str else []

    for token in accounts:
        creds = Credentials.from_authorized_user_file(token)
        service = build("gmail", "v1", credentials=creds)

        services.append(service)


def get_random_service():
    return random.choice(services)


def send_email(raw_email):

    service = get_random_service()

    encoded = base64.urlsafe_b64encode(raw_email.encode()).decode()

    service.users().messages().send(userId="me", body={"raw": encoded}).execute()
