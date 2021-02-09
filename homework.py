import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
NUMBER_TO = os.getenv('NUMBER_TO')
NUMBER_FROM = os.getenv('NUMBER_FROM')
V = os.getenv('API_V')
client = Client(ACCESS_TOKEN, AUTH_TOKEN)
BASE_URL = 'https://api.vk.com/method/users.get'
e = 'Ошибка соеденения'


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': V,
        'access_token': ACCESS_TOKEN,
        'fields': 'online'
    }
    try:
        status = requests.post(
            BASE_URL, params=params
        ).json()['response'][0]['online']
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return status


def send_sms(sms_text):
    message = client.messages.create(
        to=NUMBER_TO,
        from_=NUMBER_FROM,
        body=sms_text
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
