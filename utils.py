import boto3

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
