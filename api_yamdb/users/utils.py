import random
import string
from django.core import mail


def confirmation_code_generator():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def send_confirm_email(body, email):
    email = mail.EmailMessage(
        subject='Confirmation', body=body, to=(email,))
    email.send()
    return True
