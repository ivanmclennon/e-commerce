import os
import string
import random

from vonage import Sms
from celery import shared_task

from users.models import Seller
from .models import SMSLog


sms = Sms(
    key=os.environ.get("VONAGE_API_KEY"), secret=os.environ.get("VONAGE_API_SECRET")
)


def get_random_code(n: int = 4, chars: str = string.digits) -> str:
    """
    Returns random string sms code

    :param n: length of string
    :param chars: characters to pull from
    """
    return "".join(random.choice(chars) for _ in range(n))


@shared_task
def send_sms_task(to_number: str, sms_text: str = get_random_code()):
    """
    Send confirmation code to a phone number
    and log the message data.

    :param to_number: phone number in E164 string format
    :param sms_text: code to send in sms
    """
    sms_response = sms.send_message(
        {
            "from": os.environ.get("VONAGE_BRAND_NAME"),
            "to": to_number,
            "text": sms_text,
        }
    )

    sms_log = SMSLog(code=sms_text, response=sms_response)
    sms_log.save()
