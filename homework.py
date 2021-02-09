import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
access_token = os.getenv('ACCESS_TOKEN')
v = os.getenv('API_V')
client = Client(account_sid, auth_token)
BASE_URL = 'https://api.vk.com/method/users.get'
e = 'Ошибка соеденения'


def get_status(user_id):
    params = {
    'user_id': user_id,
    'v': v,
    'access_token': access_token,
    'fields': 'online'
    }
    try:
        status = requests.post(BASE_URL, data=params).json()['response'][0]['online']
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return status


def send_sms(sms_text):
    message = client.messages.create(
        to=os.getenv('NUM_TO'),
        from_=os.getenv('NUM_FROM'),
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
