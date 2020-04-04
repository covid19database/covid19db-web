import boto3
import random
import string

sns_client = boto3.client('sns')  # TODO: how to auth on server


def send_sms(phone_number: str, message: str, **kwargs):
    """Send an SMS to the provided phone number"""
    if not phone_number.startswith('+'):
        phone_number = '+1' + phone_number
    return sns_client.publish(
        PhoneNumber=phone_number,
        Message=message,
        **kwargs
    )


def random_code(stringLength=6):
    """Generate a random string of letters and digits.

    Totally copy-pasta'ed https://pynative.com/python-generate-random-string/
    """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
